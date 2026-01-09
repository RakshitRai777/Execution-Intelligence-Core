from pydantic import BaseModel
from typing import List, Dict


class ProcessSummaryResponse(BaseModel):
    process_id: str
    total_events: int
    status_counts: Dict[str, int]
    blocked_steps: List[str]
    responsible_teams: List[str]


class ProcessRiskResponse(BaseModel):
    process_id: str
    blocked_count: int
    delayed_count: int
    risk_level: str


class HighRiskProcessesResponse(BaseModel):
    high_risk_processes: List[ProcessRiskResponse]
