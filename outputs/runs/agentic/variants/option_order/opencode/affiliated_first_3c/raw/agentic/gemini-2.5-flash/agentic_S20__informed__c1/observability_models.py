from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class StructuredLogEntry(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resource: Dict[str, str] = Field(default_factory=dict)
    labels: Dict[str, str] = Field(default_factory=dict)
    json_payload: Dict[str, Any] = Field(default_factory=dict)


class CorrelatedLogEntry(StructuredLogEntry):
    correlation_id: str


class LogQuery(BaseModel):
    filter: str
    order_by: str = "timestamp desc"
    limit: int = 100


class LogEntry(BaseModel):
    text_payload: Optional[str] = None
    json_payload: Optional[Dict[str, Any]] = None
    severity: str
    timestamp: datetime
    resource: Dict[str, Any]
    log_name: str
