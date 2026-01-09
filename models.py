from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ExecutionEvent(BaseModel):
    process_id: str
    step: str
    status: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = datetime.utcnow()
