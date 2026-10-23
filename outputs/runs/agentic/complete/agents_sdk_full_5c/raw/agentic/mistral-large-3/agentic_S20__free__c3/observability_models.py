from pydantic import BaseModel
from typing import Dict, Any, Optional


class StructuredLogEvent(BaseModel):
    """Model for structured log events."""
    timestamp: str
    severity: str
    message: str
    attributes: Dict[str, Any]


class LogQueryResponse(BaseModel):
    """Model for log query responses."""
    logs: list
    metadata: Optional[dict] = None