from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: str = "INFO"
    message: str
    labels: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None

class QueryLogRequest(BaseModel):
    project_id: str
    filter_expression: str
    order_by: str = "timestamp desc"
    limit: int = 100

class IncidentSummaryRequest(BaseModel):
    log_entries: list[LogEntry]
    summary_length: str = "short" # "short", "medium", "long"

class TextSafetyRequest(BaseModel):
    text_content: str

class TranslateRequest(BaseModel):
    text_content: str
    target_language: str
    source_language: Optional[str] = None

class EmbedLogRequest(BaseModel):
    log_messages: list[str]
