import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class LogEntry:
    severity: str
    message: str
    resource_type: str
    resource_id: str
    timestamp: str
    labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    trace_sampled: Optional[bool] = None

@dataclasses.dataclass
class LogQuery:
    project_id: str
    filter: str
    order_by: str = "timestamp desc"
    limit: int = 100

@dataclasses.dataclass
class LogQueryResult:
    entries: List[LogEntry]
    next_page_token: Optional[str] = None

@dataclasses.dataclass
class IncidentSummaryRequest:
    log_entries: List[LogEntry]
    summary_type: str = "brief"

@dataclasses.dataclass
class SafetyCheckRequest:
    text: str

@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclasses.dataclass
class EmbeddingRequest:
    text: str
