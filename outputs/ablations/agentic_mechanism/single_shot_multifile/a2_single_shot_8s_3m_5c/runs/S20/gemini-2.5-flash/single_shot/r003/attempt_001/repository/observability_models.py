from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class LogEntry:
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    resource_type: str = "global"
    resource_labels: Dict[str, str] = field(default_factory=dict)
    labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LogQueryParameters:
    project_id: str
    log_name: Optional[str] = None
    min_severity: str = "INFO"
    time_range_seconds: int = 3600
    filter_string: Optional[str] = None
    field_filters: Optional[Dict[str, str]] = field(default_factory=dict)
    limit: int = 100

@dataclass
class LogQueryResult:
    timestamp: datetime
    severity: str
    message: str
    payload: Dict[str, Any]
    log_name: str
    resource: Dict[str, Any]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
