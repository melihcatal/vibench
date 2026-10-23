from pydantic import BaseModel
from typing import Dict, Any

class StructuredLogEvent(BaseModel):
    timestamp: str
    severity: str
    message: str
    attributes: Dict[str, Any]

class CorrelatedLogEvent(BaseModel):
    timestamp: str
    severity: str
    message: str
    correlation_id: str
    attributes: Dict[str, Any]