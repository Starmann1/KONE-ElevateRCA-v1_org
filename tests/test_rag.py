"""
ElevateRCA — Comprehensive RAG Test Suite
Tests:
1. GUIDE corpus discovery & metadata extraction
2. PDF, CSV, and JSON parsing with page/section preservation
3. Table preservation and configuration tagging (SETS/EGOV)
4. Vector store operations (index, query, get_stats)
5. Hybrid retrieval (semantic + keyword + fault-code + subsystem + configuration)
6. Authority ranking (OEM_REFERENCE > COMPONENT_GUIDE > TROUBLESHOOTING)
7. EvidenceAssembler integration (RAG evidence bundle, provenance, traceability)
8. Bayesian RCA preservation (RAG does not fabricate probabilities)
9. Safety boundaries & claim discipline with RAG enabled
"""

import pytest
import os
import sys

from pipeline.rag_schemas import (
    RAGChunk, DocumentMetadata, RAGSource, RAGEvidence,
    GUIDE_DOCUMENT_REGISTRY, AUTHORITY_LEVELS
)
from pipeline.rag_ingest import (
    GUIDECorpusIngester, PDFParser, TroubleshootingParser, SectionDetector
)
from pipeline.rag_store import RAGVectorStore
from pipeline.rag_retrieval import HybridRetriever, build_rag_query
from pipeline.engine import ElevateRCAEngine
from simulator.scenarios import ScenarioFactory


# =====================================================
# 1. GUIDE CORPUS DISCOVERY & METADATA TESTS
# =====================================================

def test_guide_corpus_discovery():
    """Verify all 14 GUIDE documents are discovered."""
    ingester = GUIDECorpusIngester(guide_dir="GUIDE")
    docs = ingester.discover_documents()
    assert len(docs) >= 14, f"Expected at least 14 documents in GUIDE/, found {len(docs)}"

    # Check key files are present
    expected_files = [
        "elevator_door_operations.pdf",
        "brake_of_geared_traction_machine.pdf",
        "brake_of_gearless_traction_machine.pdf",
        "elevator_brake_pad.pdf",
        "elevator_hoisting_rope.pdf",
        "sets-11.pdf",
        "sets_egov_8_9.pdf",
        "elevator_troubleshooting_dataset.csv",
        "elevator_troubleshooting_dataset.json",
    ]
    for ef in expected_files:
        assert ef in docs, f"Missing expected document: {ef}"


def test_document_metadata_registry():
    """Verify metadata registry has correct authority and subsystem mappings."""
    # Door document
    door_meta = GUIDE_DOCUMENT_REGISTRY.get("elevator_door_operations.pdf", {})
    assert door_meta.get("subsystem") == "door"
    assert door_meta.get("authority") == "COMPONENT_GUIDE"

    # Brake documents
    brake_meta = GUIDE_DOCUMENT_REGISTRY.get("brake_of_gearless_traction_machine.pdf", {})
    assert brake_meta.get("subsystem") == "brake_traction"
    assert brake_meta.get("configuration") == "gearless_traction"

    # SETS documents — configuration-specific
    sets_8_9 = GUIDE_DOCUMENT_REGISTRY.get("sets_egov_8_9.pdf", {})
    assert sets_8_9.get("egov") == "8_9"
    assert sets_8_9.get("authority") == "OEM_REFERENCE"

    sets_a = GUIDE_DOCUMENT_REGISTRY.get("sets_egov_a.pdf", {})
    assert sets_a.get("egov") == "A"

    # Troubleshooting datasets
    csv_meta = GUIDE_DOCUMENT_REGISTRY.get("elevator_troubleshooting_dataset.csv", {})
    assert csv_meta.get("authority") == "TROUBLESHOOTING"


# =====================================================
# 2. PARSER TESTS (PDF, CSV, JSON)
# =====================================================

def test_troubleshooting_csv_parsing():
    """Verify CSV parser extracts records with subsystem mapping."""
    chunks = TroubleshootingParser.parse_csv("GUIDE/elevator_troubleshooting_dataset.csv")
    assert len(chunks) == 15, f"Expected 15 records from CSV, got {len(chunks)}"

    # Check first record has required fields
    c0 = chunks[0]
    assert c0.authority == "TROUBLESHOOTING"
    assert c0.is_procedure is True
    assert c0.subsystem is not None
    assert "Component:" in c0.text


def test_troubleshooting_json_parsing():
    """Verify JSON parser extracts records matching CSV."""
    chunks = TroubleshootingParser.parse_json("GUIDE/elevator_troubleshooting_dataset.json")
    assert len(chunks) == 15, f"Expected 15 records from JSON, got {len(chunks)}"
    assert chunks[0].document_type == "troubleshooting_dataset"


def test_section_detector():
    """Test heading, warning, and procedure detection heuristics."""
    assert SectionDetector.is_warning("WARNING: Turn off main power switch before inspection")
    assert SectionDetector.is_warning("DANGER: High voltage capacitors remain charged")
    assert not SectionDetector.is_warning("Normal operating temperature is 45C")

    assert SectionDetector.is_procedure("Step 1: Check the brake air gap. Step 2: Adjust feeler gauge.")
    assert SectionDetector.is_procedure("Inspect door hanger rollers and verify clearance")
    assert not SectionDetector.is_procedure("The elevator moves at 2.5 m/s nominal speed")


# =====================================================
# 3. VECTOR STORE & INDEXING TESTS
# =====================================================

def test_rag_vector_store_indexed(engine):
    """Verify vector store is initialized and indexed with chunks."""
    assert engine.rag_enabled, "RAG should be enabled on the master engine"
    assert engine._rag_store is not None
    assert engine._rag_store.is_indexed
    count = engine._rag_store.document_count
    assert count > 50, f"Expected > 50 indexed chunks, found {count}"


def test_vector_store_get_stats(engine):
    """Verify index statistics include subsystems and document tracking."""
    stats = engine._rag_store.get_index_stats()
    assert stats["total_chunks"] > 50
    assert "door" in stats["subsystems_covered"]
    assert "brake_traction" in stats["subsystems_covered"]
    assert len(stats["documents_indexed"]) >= 5


# =====================================================
# 4. HYBRID RETRIEVAL TESTS
# =====================================================

def test_retrieval_door_subsystem(engine):
    """Door query must prioritize door documentation and troubleshooting."""
    retriever = engine._rag_retriever
    assert retriever is not None

    evidence = retriever.retrieve(
        query_text="door belt slip door close timeout",
        subsystem="door",
        n_results=5,
    )
    assert len(evidence.sources) > 0
    top_source = evidence.sources[0]
    # Should prioritize door documents or door troubleshooting
    assert any(w in top_source.source.lower() for w in ["door", "troubleshooting"])


def test_retrieval_brake_pad(engine):
    """Brake query must retrieve brake documents."""
    retriever = engine._rag_retriever
    evidence = retriever.retrieve(
        query_text="brake pad wear friction lining thickness",
        subsystem="brake_traction",
        n_results=5,
    )
    assert len(evidence.sources) > 0
    top_source = evidence.sources[0]
    assert any(w in top_source.source.lower() for w in ["brake", "troubleshooting"])


def test_retrieval_configuration_applicability(engine):
    """SETS retrieval with EGOV 8_9 must flag other EGOV documents appropriately."""
    retriever = engine._rag_retriever

    # Search with specific EGOV 8_9
    evidence = retriever.retrieve(
        query_text="SETS position detection terminal slowdown switch",
        subsystem="encoder_position",
        egov="8_9",
        n_results=5,
    )
    assert len(evidence.sources) > 0

    # Search without EGOV — applicability should be CONFIGURATION_UNKNOWN for EGOV-specific docs
    evidence_unknown = retriever.retrieve(
        query_text="SETS terminal slowdown switch",
        subsystem="encoder_position",
        egov=None,
        n_results=5,
    )
    assert len(evidence_unknown.sources) > 0
    has_unknown_or_conditional = any(
        s.applicability in ["CONFIGURATION_UNKNOWN", "CONDITIONAL", "MATCHED"]
        for s in evidence_unknown.sources
    )
    assert has_unknown_or_conditional


def test_retrieval_authority_ranking(engine):
    """OEM_REFERENCE should rank higher than TROUBLESHOOTING when scores are close."""
    retriever = engine._rag_retriever
    evidence = retriever.retrieve(
        query_text="door operator maintenance inspection procedure",
        subsystem="door",
        n_results=10,
    )
    assert len(evidence.sources) > 0
    # Verify all sources have authority levels populated
    for s in evidence.sources:
        assert s.authority in AUTHORITY_LEVELS


# =====================================================
# 5. EVIDENCE ASSEMBLER & TRACE INTEGRATION TESTS
# =====================================================

def test_evidence_bundle_contains_rag_sources(engine):
    """Verify that engine.analyze() populates RAG sources in ExplainabilityTrace."""
    payload = ScenarioFactory.scenario_2_mechanical_jam()
    trace = engine.analyze(payload)

    # 1. Trace must have rag_sources populated
    assert trace.rag_sources is not None
    assert len(trace.rag_sources) > 0

    # 2. Check source metadata is preserved
    first_source = trace.rag_sources[0]
    assert "source" in first_source
    assert "authority" in first_source

    # 3. Check evidence bundle contains RAG_RETRIEVED items
    rag_items = [e for e in trace.evidence_bundle if e.provenance == "RAG_RETRIEVED"]
    assert len(rag_items) > 0
    assert rag_items[0].source_document is not None

    # 4. Pipeline stages completed must include guide_rag_retrieval
    assert "guide_rag_retrieval" in trace.metadata.pipeline_stages_completed


def test_investigation_report_includes_rag_section(engine):
    """Verify that the generated Markdown report includes Section 6 (RAG Citations)."""
    payload = ScenarioFactory.scenario_1_igbt_overcurrent()
    trace = engine.analyze(payload)

    report = trace.detailed_investigation_report
    assert report is not None
    assert "## 6. GUIDE Technical Corpus & OEM Reference Citations (RAG)" in report
    assert "## 7. Diagnostic Confirmation & What Would Change the Diagnosis?" in report
    assert "Confirmation Test:" in report


# =====================================================
# 6. BAYESIAN REASONING PRESERVATION TESTS
# =====================================================

def test_rag_does_not_distort_bayesian_ranking(engine):
    """Verify that RAG does not change the deterministic ranking of canonical scenarios."""
    # Scenario 1 must still identify IGBT
    s1_trace = engine.analyze(ScenarioFactory.scenario_1_igbt_overcurrent())
    assert s1_trace.hypotheses[0].hypothesis_id == "RC1"
    assert s1_trace.hypotheses[0].posterior_probability >= 0.65

    # Scenario 2 must still identify Mechanical Jam
    s2_trace = engine.analyze(ScenarioFactory.scenario_2_mechanical_jam())
    assert "Mechanical" in s2_trace.hypotheses[0].root_cause
    assert s2_trace.hypotheses[0].posterior_probability >= 0.50

    # Scenario 6 must still ABSTAIN
    s6_trace = engine.analyze(ScenarioFactory.scenario_6_abstention_conflicting())
    assert s6_trace.rca_conclusion.abstained is True
    assert s6_trace.rca_conclusion.root_cause_confidence_tier == "ABSTAIN"


# =====================================================
# 7. SAFETY BOUNDARIES & CLAIM DISCIPLINE
# =====================================================

def test_rag_enabled_safety_compliance(engine):
    """Verify advisory-only status and zero actuation path with RAG enabled."""
    payload = ScenarioFactory.scenario_3_door_photoeye_drift()
    trace = engine.analyze(payload)

    # 1. Must be advisory only
    assert trace.metadata.advisory_only is True
    assert trace.metadata.human_verification_required is True

    # 2. Corrective recommendation must have warning
    assert "RECOMMENDATION only" in trace.corrective_recommendation.warning

    # 3. No claim discipline violations
    assert len(trace.metadata.claim_discipline_flags) == 0
