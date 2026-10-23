from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: Literal['DEFAULT', 'DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'ALERT', 'EMERGENCY'] = 'INFO'
    message: str
    resource_type: str = 'global'
    resource_labels: Dict[str, str] = {}
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    correlation_id: Optional[str] = None

class LogQuery(BaseModel):
    project_id: str
    filter: str
    order_by: str = "timestamp desc"
    page_size: int = 100
    page_token: Optional[str] = None

class LogQueryResult(BaseModel):
    entries: List[LogEntry]
    next_page_token: Optional[str] = None

class IncidentSummaryRequest(BaseModel):
    log_entries: List[str]

class IncidentSummaryResponse(BaseModel):
    summary: str

class SafetyCheckRequest(BaseModel):
    text: str

class SafetyCheckResponse(BaseModel):
    is_safe: bool
    reasons: List[str] = []

class TranslateRequest(BaseModel):
    text: str
    target_language_code: str

class TranslateResponse(BaseModel):
    translated_text: str

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]
