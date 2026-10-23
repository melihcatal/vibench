from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional


@dataclass
class StructuredLogEntry:
    message: str
    severity: str = "INFO"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CorrelatedLogEntry:
    message: str
    correlation_id: str
    severity: str = "INFO"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ErrorLogQuery:
    project_id: str
    min_severity: str = "ERROR"
    time_range_minutes: int = 60


@dataclass
class RecentLogQuery:
    project_id: str
    log_name: str
    time_range_minutes: int = 60
    field_filters: Dict[str, str] = field(default_factory=dict)
