# ElevateRCA — KONE Diagnostic Intelligence & Root Cause Analysis

> **Auditable, Evidence-Driven Fault Isolation Layer for KONE MonoSpace / MiniSpace Elevators (EcoDisc PMSM Motors)**

ElevateRCA operates strictly as a **read-only advisory intelligence layer** that sits outside the elevator safety-control loop. It observes multi-rate telemetry and cascading alarms, correlates fault episodes, traverses 6-subsystem fault trees, computes calibrated Bayesian posterior probabilities over competing hypotheses, explicitly eliminates alternative causes using negative evidence, and generates auditable `ExplainabilityTrace` artifacts for mandatory technician verification.

---

## 🛡️ Absolute Safety Boundaries (Part 2)

- ❌ **Zero Hardware Control**: Never issues commands to motors, drives, brakes, door operators, or actuators.
- ❌ **Independent Safety Chain**: Never overrides, resets, or bypasses the hardwired relay safety circuit.
- ❌ **Read-Only Advisory Role**: Operates strictly post-trip to assist human diagnostics.
- ❌ **No Invented Claims or Actions**: Corrective actions are strictly drawn from an OEM-approved SOP lookup table.
- ❌ **Principled Abstention**: Explicitly abstains when evidence is conflicting or degraded (<50% sensor quality).
- ✅ **Mandatory Human Verification**: Every output enforces technician sign-off before clearing any fault.

---

## 📐 Architecture & 5-Stage Reasoning Pipeline (Part 4)

```
KONE Software Output (Alarms + Telemetry + History)
                    │
                    ▼
 ┌─────────────────────────────────────────────────────────┐
 │ STAGE 1: Signal Triage & Anomaly Detection              │
 │ • EWMA / CUSUM tracking against engineering baselines   │
 │ • Anomaly classification & operating-state contextualization │
 │ • Sensor quality gating (bad/missing = zero weight)    │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │ STAGE 2: Alarm Cascade Correlation                      │
 │ • ISA-18.2 15-second temporal clustering window         │
 │ • Causal chain reconstruction (Primary vs Consequential)│
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │ STAGE 3: Evidence Retrieval & Assembly                  │
 │ • Provenance tags: [MEASURED], [LOGGED], [HISTORICAL]   │
 │ • Positive vs Negative support labeling                 │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │ STAGE 4: Fault Tree Traversal & Bayesian Ranking        │
 │ • 6 Subsystems: Drive/Motor, Door, Brake, Encoder,      │
 │   Safety Chain, Sensors/Environmental                   │
 │ • 4-Step Q1-Q4 discipline with True Negatives           │
 │ • Bayesian posterior probabilities summing to 100%     │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
 ┌─────────────────────────────────────────────────────────┐
 │ STAGE 5: Confidence Decision & Dual Synthesis           │
 │ • Dual Scoring: root_cause_confidence & action_confidence│
 │ • Calibrated Tiers: HIGH (≥0.75), MEDIUM, LOW, ABSTAIN │
 │ • Dual-View Output: Technician SOP & Manager Summary    │
 └──────────────────────────┬──────────────────────────────┘
                            │
                            ▼
               Auditable ExplainabilityTrace JSON
```

---

## 🚀 Quickstart & Usage

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Run Test Suite (Scenario Benchmarks)
```bash
python -m pytest -v
```

### 3. Launch ElevateRCA API & Interactive Web Dashboard
```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000`** in your browser to access the live glassmorphic diagnostic dashboard.

---

## 🔬 6 Canonical Scenarios Implemented (Part 6)

1. **Scenario 1: IGBT Power Electronics Failure** (`KONE-MONO-501`)
   - *Pattern*: `motor_current_rms` +136.7% step spike, `igbt_temp` elevated, drive self-test `FAILED`.
   - *Result*: Ranked #1 (97% posterior), Brake Drag and Mechanical Obstruction eliminated.
2. **Scenario 2: Hoistway / Guide Rail Mechanical Jam** (`KONE-MONO-502`)
   - *Pattern*: `motor_current_rms` +90%, `vibration_rms` +250%, drive self-test `PASSED`.
   - *Result*: Mechanical Obstruction ranked #1, IGBT eliminated due to healthy drive electronics.
3. **Scenario 3: Door 3D Light Curtain Optical Drift** (`KONE-MINI-301`)
   - *Pattern*: `door_cycle_time_ms` +58.9%, recurring reopens at varying door positions.
   - *Result*: Light Curtain Degradation ranked #1, fixed physical sill jam eliminated.
4. **Scenario 4: EcoDisc Motor Encoder Pulse Loss** (`KONE-MONO-504`)
   - *Pattern*: Leveling deviation +325%, position divergence +580%, independent sensor normal.
   - *Result*: Optical Encoder Degradation ranked #1.
5. **Scenario 5: Brake Release Timing Violation** (`KONE-MONO-505`)
   - *Pattern*: Brake release delay 360ms (+140%), normal motor torque, position drift.
   - *Result*: Brake Release Timing ranked #1.
6. **Scenario 6: Principled Abstention Benchmark** (`KONE-MONO-506`)
   - *Pattern*: Conflicting signals, degraded temperature sensor quality (`bad`/`missing`).
   - *Result*: Explicit abstention triggered (`ABSTAIN`), routes to physical multi-point inspection.

---

## 📡 REST API Endpoints

- `GET  /api/v1/health`: Safety state, isolation verification, engine status, and RAG index health.
- `POST /api/v1/analyze`: Accepts raw `KONEFaultInput` and returns `ExplainabilityTrace`.
- `GET  /api/v1/scenarios`: Returns catalog of 6 canonical scenarios.
- `POST /api/v1/scenarios/{scenario_id}/run`: Executes canonical scenario on demand.
- `POST /api/v1/human-review`: Records digital technician verification and audit sign-off.
- `GET  /api/v1/knowledge/sources`: Vector store statistics, indexed chunks, and registered GUIDE documents.
- `POST /api/v1/knowledge/reindex`: Re-indexes the GUIDE corpus into ChromaDB on demand.
- `GET  /api/v1/diagnosis/{id}/sources`: Retrieved RAG evidence sources cited in a specific diagnostic trace.
- `GET  /api/v1/telemetry-samples`: Catalog of all 20 door problem telemetry datasets.
- `GET  /api/v1/error-matrix`: 2D Error Table Matrix mapping Ranks F1–F7 & Columns 1–8.
- `GET  /api/v1/oem-guides`: Quantitative engineering limits and field troubleshooting cases.

---

## 📚 Technical Documentation

- [`docs/RAG_GUIDE_CORPUS.md`](docs/RAG_GUIDE_CORPUS.md) — 14-document inventory, metadata schema, and 5-tier authority hierarchy.
- [`docs/RAG_ARCHITECTURE.md`](docs/RAG_ARCHITECTURE.md) — Ingestion, ChromaDB vector store, hybrid retrieval, and evidence integration.
- [`docs/RAG_RETRIEVAL_EVALUATION.md`](docs/RAG_RETRIEVAL_EVALUATION.md) — Precision benchmarks, configuration filtering tests, and ground-truth preservation.
- [`docs/TECHNICIAN_DIAGNOSTIC_LOOP.md`](docs/TECHNICIAN_DIAGNOSTIC_LOOP.md) — Human review protocol, confirmation tests, and observation interpretation.
- [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) — Master completion matrix and 25-test verification report.

---

## 👥 Authors & Attribution

* **Project**: KONE Elevate — Autonomous Fault Isolation & Bayesian RCA (ElevateRCA)
* **Developer**: **Arul Amudhan G & Sanjay Krshna G**
* **Organization**: Rajalakshmi Engineering College
* **Hackathon**: KONE Elevate 2026
* **Repository**: [https://github.com/Starmann1/ElevateRCA.git](https://github.com/Starmann1/KONE-ElevateRCA-v1_org.git)

---
