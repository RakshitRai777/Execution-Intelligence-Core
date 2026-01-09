from fastapi import FastAPI, HTTPException
from models import ExecutionEvent
from core import ExecutionIntelligenceCore
from schemas import (
    ProcessSummaryResponse,
    ProcessRiskResponse,
    HighRiskProcessesResponse
)

app = FastAPI(
    title="Execution Intelligence Core",
    description="Deterministic execution intelligence engine for process monitoring, risk assessment, and operational insights.",
    version="0.6.0"
)

core = ExecutionIntelligenceCore()


# -------------------------
# Ingestion
# -------------------------

@app.post(
    "/event",
    summary="Ingest execution event",
    description="Ingests a single execution event and returns an intelligence-based explanation."
)
def ingest_event(event: ExecutionEvent):
    explanation = core.process_event(event)
    return {"explanation": explanation}


# -------------------------
# Health
# -------------------------

@app.get(
    "/health",
    summary="Health check",
    description="Returns service health status."
)
def health():
    return {"status": "alive"}


# -------------------------
# Process Insights
# -------------------------

@app.get(
    "/process/{process_id}/summary",
    response_model=ProcessSummaryResponse,
    summary="Get process execution summary",
    description="Returns aggregated execution insights for a given process, including status counts, blocked steps, and responsible teams."
)
def process_summary(process_id: str):
    result = core.get_process_summary(process_id)
    if not result:
        raise HTTPException(status_code=404, detail="Process not found")
    return result


@app.get(
    "/process/{process_id}/risk",
    response_model=ProcessRiskResponse,
    summary="Get process risk assessment",
    description="Returns deterministic risk evaluation for a process based on historical blocked and delayed events."
)
def process_risk(process_id: str):
    result = core.get_process_risk(process_id)
    if not result:
        raise HTTPException(status_code=404, detail="Process not found")
    return result


# -------------------------
# System Insights
# -------------------------

@app.get(
    "/stats/high-risk-processes",
    response_model=HighRiskProcessesResponse,
    summary="List high-risk processes",
    description="Returns all processes currently classified as HIGH RISK based on execution history."
)
def high_risk_processes():
    return {
        "high_risk_processes": core.get_high_risk_processes()
    }
