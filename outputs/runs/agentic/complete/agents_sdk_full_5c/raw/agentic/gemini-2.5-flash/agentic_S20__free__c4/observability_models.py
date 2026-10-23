from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Any, Dict

@dataclass
class LogEntryPayload:
    """
    Represents a normalized payload for a structured log entry.
    """
    message: str
    severity: str = "INFO"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    # Additional structured fields
    json_data: Dict[str, Any] = field(default_factory=dict)
    resource_type: str = "global"
    resource_labels: Dict[str, str] = field(default_factory=dict)
    trace_id: Optional[str] = None

@dataclass
class LogQueryParameters:
    """
    Represents parameters for querying logs.
    """
    log_name: str
    project_id: str
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None
    severity_min: Optional[str] = None
    text_filter: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 100
    order_by: str = "timestamp desc"


@dataclass
class ParsedLogEntry:
    """
    Represents a normalized log entry parsed from a logging service response.
    """
    log_name: str
    severity: str
    timestamp: datetime
    payload: Any # Can be str (textPayload) or dict (jsonPayload)
    resource_type: str
    resource_labels: Dict[str, str]
    trace: Optional[str] = None
    span_id: Optional[str] = None
    insert_id: Optional[str] = None
