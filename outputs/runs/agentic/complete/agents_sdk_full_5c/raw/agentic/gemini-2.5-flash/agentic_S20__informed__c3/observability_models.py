from dataclasses import dataclass, field
import datetime
from typing import Optional, Dict, Any

@dataclass
class LogEntry:
    """Represents a standardized log entry."""
    message: str
    severity: str = "INFO"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    resource_type: Optional[str] = None
    resource_labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    correlation_id: Optional[str] = None

@dataclass
class LogQuery:
    """Represents parameters for querying logs."""
    project_id: str
    log_name: str
    time_range_minutes: int = 60
    severity_filter: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    page_size: int = 10
    order_by: str = "timestamp desc" # "timestamp desc" or "timestamp asc"

@dataclass
class SummarizationRequest:
    """Represents a request for summarizing log data."""
    log_data: str
    summary_length: str = "short" # e.g., "short", "medium", "detailed"
    target_audience: str = "incident responder"

@dataclass
class SafetyCheckRequest:
    """Represents a request for checking log text safety."""
    text_content: str
    client_ip: Optional[str] = None # For Perspective API
    session_id: Optional[str] = None # For Perspective API

@dataclass
class TranslationRequest:
    """Represents a request for translating log messages."""
    text_content: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class EmbeddingRequest:
    """Represents a request for generating text embeddings."""
    text_content: str
