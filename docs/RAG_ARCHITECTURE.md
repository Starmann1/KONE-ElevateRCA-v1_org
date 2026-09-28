# ElevateRCA RAG Architecture Specification

## 1. High-Level Architectural Positioning

ElevateRCA uses Retrieval-Augmented Generation (RAG) strictly as an **evidence retrieval and ground-truth verification engine**, not as an unconstrained generative reasoning layer. The system operates strictly as a **read-only advisory diagnostic intelligence system** outside the elevator safety circuit.

```
       [Raw KONE Software Fault Event]
                     │
                     ▼
         [Stage 1: Signal Triage]
           EWMA / CUSUM baselining & state-aware classification
                     │
                     ▼
         [Stage 2: Alarm Correlation]
           ISA-18.2 temporal clustering & causal cascade suppression
                     │
                     ▼
         [Stage 3: Evidence Retrieval & Assembly]
     ┌───────────────────────┬────────────────────────┐
     │ Telemetry [MEASURED]  │ Alarms [LOGGED]        │
     │ Operating State       │ Maintenance [HISTORICAL│
     │ Free Text [LOGGED]    │ GUIDE RAG Technical    │
     └───────────────────────┴────────────────────────┘
                     │
                     ▼
         [Stage 4: Bayesian RCA Engine]
           Fault-tree traversal, negative evidence penalties,
           prior repeat-repair boost, normalized posteriors
                     │
                     ▼
         [Stage 5: Synthesis & Decision Gate]
           Calibrated dual confidence, principled abstention,
           approved OEM SOP lookup, 24-section technician report
                     │
                     ▼
         [Safety Guardrails Verification]
           Claim discipline regex check, hard prohibition of control commands
                     │
                     ▼
        [Auditable ExplainabilityTrace JSON & Markdown Report]
```

---

## 2. RAG Component Breakdown

### 2.1 Ingestion Engine (`pipeline/rag_ingest.py`)
- **Document Discovery:** Automatically scans the `GUIDE/` directory for technical manuals.
- **PyMuPDF Parser:** Page-accurate text extraction, preserving headings, bulleted steps, and structured tables.
- **Troubleshooting Parser:** Converts structured CSV/JSON records (`ELV-001` through `ELV-015`) into semantic symptom-cause chunks.
- **Section & Semantic Chunking:** Paragraph-aware windowing (800 characters, 100 overlap) with section headings attached.
- **Metadata Enrichment:** Maps each chunk to subsystem, component, document authority, and configuration parameters (e.g. `EGOV 8/9`, `SETS-11`).

### 2.2 Vector Store & Embedding (`pipeline/rag_store.py`)
- **Engine:** ChromaDB `PersistentClient` in `.chroma_db/` (per ADR-009).
- **Embedding Model:** `all-MiniLM-L6-v2` via native ChromaDB `SentenceTransformerEmbeddingFunction`.
- **Offline Optimization:** `HF_HUB_OFFLINE=1` prevents slow network roundtrips to Hugging Face Hub during initialization.
- **Sub-Millisecond Keyword Search:** Implemented using ChromaDB's native `collection.get(where_document={"$contains": keyword})`, eliminating redundant neural embedding for keyword lookups.

### 2.3 Hybrid Retrieval Engine (`pipeline/rag_retrieval.py`)
Combines 5 search vectors into an authority-ranked retrieval result:
1. **Semantic Search with Subsystem Filter:** Direct cosine similarity against subsystem-filtered chunks.
2. **Broad Semantic Search:** Fallback semantic context if filtered results are sparse.
3. **Keyword Search for Fault Codes:** Exact match for KONE controller codes (`F11`, `F14`, `F24`, etc.).
4. **Component Term Matching:** Exact keyword matching on mechanical and electrical component terms.
5. **Configuration-Specific Filtering:** Targeted matching for speed governor settings (`EGOV 8_9`, `A`, `B`, `D_E`, `F`).

### 2.4 Authority Ranking Formula
$$\text{FinalScore} = \text{CosineSimilarity} + \text{AuthBoost} + \text{SubsystemBoost} + \text{ComponentBoost} + \text{ConfigBoost} + \text{ContentBoost}$$
Where:
- $\text{AuthBoost} = (6 - \text{AuthorityLevel}) \times 0.05$ (Tier 1 gets $+0.25$, Tier 3 gets $+0.15$)
- $\text{SubsystemBoost} = +0.15$ for exact subsystem match
- $\text{ComponentBoost} = +0.10$ for component term match
- $\text{ConfigBoost} = +0.20$ for exact configuration match, $-0.30$ for conflicting configuration
- $\text{ContentBoost} = +0.05$ for step-by-step procedures and quantitative tables

---

## 3. Evidence Integration Discipline

1. **RAG Does Not Fabricate Probabilities:**
   - Bayesian posterior ranking in Stage 4 is computed strictly from the mathematically grounded fault tree (`failure_modes.yaml`) and triaged sensor telemetry.
   - RAG evidence enters the `EvidenceBundle` with provenance `RAG_RETRIEVED` and serves as external grounding in the explanation and SOP lookup.
2. **Corrective Actions Are Grounded:**
   - Field actions must match approved OEM standard operating procedures from `knowledge/corrective_actions.yaml`.
   - RAG excerpts provide step-by-step guidance and clearance specifications, but cannot invent unauthorized field procedures.
3. **Negative Evidence Support:**
   - When a physical inspection observation is reported by a technician ("roller rotates freely"), it is ingested with `support_type="NEGATIVE"` and actively penalizes the candidate hypothesis in Bayesian updates.
