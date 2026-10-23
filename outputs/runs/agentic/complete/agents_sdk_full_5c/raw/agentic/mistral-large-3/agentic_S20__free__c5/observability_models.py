from pydantic import BaseModel
from typing import Dict, Optional

class StructuredLogEvent(BaseModel):
    timestamp: str
    severity: str
    message: str
    attributes: Dict

class CorrelatedLogEvent(StructuredLogEvent):
    correlation_id: str

class LogQueryResponse(BaseModel):
    logs: list
    metadata: Optional[dict] = None