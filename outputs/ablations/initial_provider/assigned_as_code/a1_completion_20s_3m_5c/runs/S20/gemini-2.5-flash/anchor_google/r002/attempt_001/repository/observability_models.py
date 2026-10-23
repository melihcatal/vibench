from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class LogEntry(BaseModel):
    timestamp: datetime
    severity: str
    message: str
    resource_type: str
    resource_labels: Dict[str, str]
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    insert_id: Optional[str] = None

class QueryLogRequest(BaseModel):
    project_id: str
    filter_expression: str
    order_by: str = "timestamp desc"
    page_size: int = 100
    page_token: Optional[str] = None

class QueryLogResponse(BaseModel):
    entries: List[LogEntry]
    next_page_token: Optional[str] = None

class CorrelatedLogEvent(BaseModel):
    event: Dict[str, Any]
    log_name: str
    project_id: str
    correlation_id: str
    timestamp_ms: Optional[float] = None

class IncidentSummaryRequest(BaseModel):
    project_id: str
    query: str
    time_range_hours: int = 1

class IncidentSummaryResponse(BaseModel):
    summary: str
    error_count: int
    log_entries: List[LogEntry]

class SafetyCheckRequest(BaseModel):
    project_id: str
    text_content: str

class SafetyCheckResponse(BaseModel):
    is_safe: bool
    reasons: List[str]

class TranslateRequest(BaseModel):
    project_id: str
    text_content: str
    target_language: str

class TranslateResponse(BaseModel):
    translated_text: str

class EmbeddingRequest(BaseModel):
    project_id: str
    text_content: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]
