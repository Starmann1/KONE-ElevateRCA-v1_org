"""
ElevateRCA — FastAPI REST API Server
Provides high-performance diagnostic endpoints, scenario runners, and human review gates.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import json
import yaml

from pipeline.schemas import KONEFaultInput, ExplainabilityTrace
from pipeline.engine import ElevateRCAEngine
from simulator.scenarios import ScenarioFactory


app = FastAPI(
    title="ElevateRCA API",
    description="Evidence-driven Fault Isolation and Root Cause Analysis for KONE Elevators",
    version="1.0.0"
)

# Enable CORS for local development and web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ElevateRCAEngine(
    failure_modes_path="knowledge/failure_modes.yaml",
    causal_links_path="knowledge/causal_links.yaml",
    corrective_actions_path="knowledge/corrective_actions.yaml"
)

# In-memory store for audit logs, human reviews, and recent diagnostic traces
REVIEW_LOGS: List[Dict[str, Any]] = []
DIAGNOSIS_STORE: Dict[str, ExplainabilityTrace] = {}


class HumanReviewSubmission(BaseModel):
    investigation_id: str
    decision: str = Field(..., description="ACCEPTED | EDITED | REJECTED")
    technician_name: str
    technician_badge: str
    notes: Optional[str] = None
    override_hypothesis_id: Optional[str] = None


@app.get("/api/v1/health")
def get_health():
    return {
        "status": "HEALTHY",
        "role": "READ_ONLY_ADVISORY_INTELLIGENCE",
        "safety_chain_state": "INDEPENDENT_HARDWIRED",
        "control_loop_isolated": True,
        "engine": "ElevateRCA Bayesian Multi-Hypothesis v1.0.0",
        "rag_enabled": engine.rag_enabled,
        "rag_corpus_chunks": engine._rag_store.document_count if engine._rag_store else 0
    }


@app.post("/api/v1/analyze", response_model=ExplainabilityTrace)
def analyze_fault(fault_input: KONEFaultInput):
    """Executes the 5-Stage RCA Pipeline and returns an auditable ExplainabilityTrace."""
    try:
        trace = engine.analyze(fault_input)
        DIAGNOSIS_STORE[trace.investigation_id] = trace
        return trace
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic error: {str(e)}")


# Production Incident Catalog
INCIDENT_DATABASE = {
    "INC-2026-0941": {
        "id": "INC-2026-0941",
        "title": "EcoDisc Drive Motor Overcurrent Trip",
        "asset_id": "KONE-MONO-501",
        "location": "North Tower - Passenger Car 1",
        "model": "KONE MonoSpace 500 (EcoDisc MX10)",
        "subsystem": "drive_motor",
        "severity": "CRITICAL",
        "factory": ScenarioFactory.scenario_1_igbt_overcurrent
    },
    "INC-2026-0942": {
        "id": "INC-2026-0942",
        "title": "Mid-Shaft Hoistway Guide Rail Mechanical Jam",
        "asset_id": "KONE-MONO-502",
        "location": "South Tower - Service Lift 2",
        "model": "KONE MonoSpace 700",
        "subsystem": "drive_motor",
        "severity": "CRITICAL",
        "factory": ScenarioFactory.scenario_2_mechanical_jam
    },
    "INC-2026-0943": {
        "id": "INC-2026-0943",
        "title": "3D Light Curtain Optical Sensor Drift & Door Timeout",
        "asset_id": "KONE-MINI-301",
        "location": "Main Hospital Wing - Elevator 3",
        "model": "KONE MiniSpace",
        "subsystem": "door",
        "severity": "WARNING",
        "factory": ScenarioFactory.scenario_3_door_photoeye_drift
    },
    "INC-2026-0944": {
        "id": "INC-2026-0944",
        "title": "EcoDisc Optical Encoder Pulse Divergence & Leveling Fault",
        "asset_id": "KONE-MONO-504",
        "location": "Commercial Hub - Express Lift A",
        "model": "KONE MonoSpace 500",
        "subsystem": "encoder_position",
        "severity": "WARNING",
        "factory": ScenarioFactory.scenario_4_encoder_fault
    },
    "INC-2026-0945": {
        "id": "INC-2026-0945",
        "title": "EcoDisc Mechanical Brake Release Delay & Position Drift",
        "asset_id": "KONE-MONO-505",
        "location": "West Plaza - Car 5",
        "model": "KONE MonoSpace 500",
        "subsystem": "brake_traction",
        "severity": "CRITICAL",
        "factory": ScenarioFactory.scenario_5_brake_drag_timing
    },
    "INC-2026-0946": {
        "id": "INC-2026-0946",
        "title": "Sensor Signal Discrepancy & Degraded Telemetry Quality",
        "asset_id": "KONE-MONO-506",
        "location": "East Wing - Cargo Lift 1",
        "model": "KONE MonoSpace 500",
        "subsystem": "drive_motor",
        "severity": "WARNING",
        "factory": ScenarioFactory.scenario_6_abstention_conflicting
    }
}


@app.get("/api/v1/incidents")
def list_incidents():
    """Returns active elevator fault incidents logged in the fleet telemetry network."""
    return [
        {
            "id": inc["id"],
            "title": inc["title"],
            "asset_id": inc["asset_id"],
            "location": inc["location"],
            "model": inc["model"],
            "subsystem": inc["subsystem"],
            "severity": inc["severity"]
        }
        for inc in INCIDENT_DATABASE.values()
    ]


@app.get("/api/v1/incidents/{incident_id}/payload", response_model=KONEFaultInput)
def get_incident_payload(incident_id: str):
    """Retrieves the raw KONE software output payload for an active incident."""
    if incident_id not in INCIDENT_DATABASE:
        raise HTTPException(status_code=404, detail="Incident ID not found.")
    return INCIDENT_DATABASE[incident_id]["factory"]()


@app.post("/api/v1/incidents/{incident_id}/analyze", response_model=ExplainabilityTrace)
def analyze_incident(incident_id: str):
    """Executes the 5-Stage RCA Pipeline for an active incident."""
    payload = get_incident_payload(incident_id)
    trace = engine.analyze(payload)
    DIAGNOSIS_STORE[trace.investigation_id] = trace
    return trace


@app.get("/api/v1/audit-log")
def get_audit_log():
    """Retrieves full human verification audit log trail."""
    return REVIEW_LOGS


# Backward compatible aliases
@app.get("/api/v1/scenarios")
def list_scenarios_alias():
    return list_incidents()

@app.post("/api/v1/scenarios/{scenario_id}/run", response_model=ExplainabilityTrace)
def run_scenario_alias(scenario_id: str):
    # Map scenario_1 -> INC-2026-0941, etc.
    mapping = {
        "scenario_1": "INC-2026-0941",
        "scenario_2": "INC-2026-0942",
        "scenario_3": "INC-2026-0943",
        "scenario_4": "INC-2026-0944",
        "scenario_5": "INC-2026-0945",
        "scenario_6": "INC-2026-0946"
    }
    target_id = mapping.get(scenario_id, scenario_id)
    return analyze_incident(target_id)


@app.post("/api/v1/human-review")
def submit_human_review(review: HumanReviewSubmission):
    """Logs technician verification / approval for auditable traceability."""
    record = {
        "investigation_id": review.investigation_id,
        "decision": review.decision,
        "technician_name": review.technician_name,
        "technician_badge": review.technician_badge,
        "notes": review.notes,
        "override_hypothesis_id": review.override_hypothesis_id,
        "audit_timestamp": review.investigation_id
    }
    REVIEW_LOGS.append(record)
    return {
        "status": "RECORDED",
        "message": f"Human review decision '{review.decision}' successfully committed to audit log.",
        "log_entry": record
    }


@app.get("/api/v1/telemetry-samples")
def list_telemetry_samples(subsystem: Optional[str] = None):
    """Lists sample telemetry scenarios generated from KONE Fault Dictionary (filter by subsystem)."""
    catalog_path = "sample_telemetry/TELEMETRY_CATALOG.json"
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if subsystem:
                sub_lower = subsystem.lower()
                return [s for s in data if s.get("subsystem", "").lower() == sub_lower or sub_lower in s.get("filename", "").lower()]
            return data
    return []


@app.get("/api/v1/telemetry-samples/{filename}")
def get_telemetry_sample(filename: str):
    """Fetches the raw JSON telemetry payload for a specific sample file."""
    # Ensure safe filename
    safe_name = os.path.basename(filename)
    file_path = os.path.join("sample_telemetry", safe_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Telemetry sample file not found.")


@app.get("/api/v1/error-matrix")
def get_error_matrix():
    """Returns the complete 2D Error Table Matrix mapping Ranks F1-F7 & Columns 1-8."""
    matrix_path = "knowledge/kone_error_matrix.yaml"
    if os.path.exists(matrix_path):
        with open(matrix_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


@app.get("/api/v1/error-matrix/{code}")
def get_error_matrix_code(code: str):
    """Fetches diagnostic details for a specific F-code (e.g. F11, F14, F15, F22, F33, F54, F68)."""
    matrix = get_error_matrix()
    target_code = code.upper()
    for err in matrix.get("error_codes", []):
        if err.get("code") == target_code:
            return err
    raise HTTPException(status_code=404, detail=f"Error code '{code}' not found in Error Table Matrix.")


@app.get("/api/v1/oem-guides")
def get_oem_guides():
    """Returns OEM engineering standards and field troubleshooting records."""
    guides_path = "knowledge/oem_guides.yaml"
    if os.path.exists(guides_path):
        with open(guides_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


# =====================================================
# RAG KNOWLEDGE CORPUS ENDPOINTS
# =====================================================

@app.get("/api/v1/knowledge/sources")
def get_knowledge_sources():
    """Returns RAG vector store statistics and registered GUIDE documents."""
    if not engine.rag_enabled or not engine._rag_store:
        return {"status": "RAG_DISABLED", "documents": [], "total_chunks": 0}
    stats = engine._rag_store.get_index_stats()
    stats["status"] = "INDEXED" if engine._rag_store.is_indexed else "NOT_INDEXED"
    from pipeline.rag_schemas import GUIDE_DOCUMENT_REGISTRY
    stats["registry"] = GUIDE_DOCUMENT_REGISTRY
    return stats


@app.post("/api/v1/knowledge/reindex")
def reindex_knowledge():
    """Forces re-indexing of the GUIDE corpus documents into ChromaDB."""
    if not engine._rag_store:
        raise HTTPException(status_code=503, detail="RAG system not initialized.")
    result = engine.reindex_guide_corpus()
    return {"message": "Re-indexing complete", "stats": result}


@app.get("/api/v1/diagnosis/{investigation_id}/sources")
def get_diagnosis_sources(investigation_id: str):
    """Fetches RAG sources cited in a specific diagnostic investigation."""
    if investigation_id in DIAGNOSIS_STORE:
        trace = DIAGNOSIS_STORE[investigation_id]
        return {
            "investigation_id": investigation_id,
            "elevator_id": trace.elevator_id,
            "rag_sources": getattr(trace, "rag_sources", []) or []
        }
    raise HTTPException(status_code=404, detail=f"Investigation ID '{investigation_id}' not found in active session.")





# Static frontend mounting if directory exists
if os.path.exists("dashboard/dist/index.html"):
    @app.get("/")
    async def serve_index():
        return FileResponse("dashboard/dist/index.html")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api"):
            raise HTTPException(status_code=404)
        file_path = os.path.join("dashboard/dist", full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("dashboard/dist/index.html")
