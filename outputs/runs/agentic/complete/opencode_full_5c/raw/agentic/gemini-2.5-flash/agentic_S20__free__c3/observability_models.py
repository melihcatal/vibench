from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class StructuredLogEntry(BaseModel):
    message: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resource_type: str = "global"
    resource_labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None


class CorrelatedLogEntry(BaseModel):
    message: str
    correlation_id: str
    severity: str = "INFO"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resource_type: str = "global"
    resource_labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None


class LogQueryRequest(BaseModel):
    filter: str
    order_by: str = "timestamp desc"
    limit: int = 100


class IncidentSummaryRequest(BaseModel):
    project_id: str
    log_name: str
    time_range_seconds: int = 3600  # Last 1 hour


class SafetyCheckRequest(BaseModel):
    text: str


class TranslateRequest(BaseModel):
    text: str
    target_language: str


class EmbeddingRequest(BaseModel):
    text: List[str]
