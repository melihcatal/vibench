import dataclasses
import datetime
from typing import Any, Dict, Optional, List


@dataclasses.dataclass
class LogEntry:
    severity: str
    message: str
    timestamp: datetime.datetime = dataclasses.field(
        default_factory=datetime.datetime.utcnow
    )
    labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class StructuredLogEntry:
    log_name: str
    resource_type: str
    resource_labels: Dict[str, str]
    json_payload: Dict[str, Any]
    severity: str = "INFO"


@dataclasses.dataclass
class CorrelatedLogEntry:
    log_name: str
    resource_type: str
    resource_labels: Dict[str, str]
    entries: List[Dict[str, Any]]


@dataclasses.dataclass
class LogErrorQuery:
    project_id: str
    severity: str = "ERROR"
    time_range_seconds: int = 3600  # Last hour


@dataclasses.dataclass
class LogQuery:
    project_id: str
    filter_string: str
    time_range_seconds: int = 3600  # Last hour
