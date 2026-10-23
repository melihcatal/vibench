from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class StructuredLogEntry(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resource_type: str = "global"
    resource_labels: Dict[str, str] = Field(default_factory=dict)
    labels: Dict[str, str] = Field(default_factory=dict)
    json_payload: Optional[Dict[str, Any]] = None


class LogQuery(BaseModel):
    filter: str
    order_by: str = "timestamp desc"
    limit: int = 100


class LogEntryResponse(BaseModel):
    timestamp: datetime
    severity: str
    message: str
    resource_type: str
    resource_labels: Dict[str, str]
    labels: Dict[str, str]
    json_payload: Optional[Dict[str, Any]] = None
    insert_id: str
    log_name: str


class CorrelatedLogEntry(BaseModel):
    correlation_id: str
    message: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    service_context: Dict[str, str] = Field(default_factory=dict)
    json_payload: Optional[Dict[str, Any]] = None
