from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

class LogSeverity(Enum):
    DEFAULT = "DEFAULT"
    DEBUG = "DEBUG"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    ALERT = "ALERT"
    EMERGENCY = "EMERGENCY"
    UNKNOWN = "UNKNOWN"

@dataclass
class StructuredLogEntry:
    message: str
    severity: LogSeverity = LogSeverity.INFO
    component: str = "default"
    version: str = "1.0.0"
    data: Optional[dict[str, Any]] = field(default_factory=dict)

@dataclass
class QueryResult:
    log_id: str
    timestamp: str
    severity: str
    message: str
    resource_type: str
    full_entry: dict[str, Any] = field(default_factory=dict)

@dataclass
class IncidentSummary:
    title: str
    impact_assessment: str
    root_cause_hint: Optional[str] = None
    suggested_actions: Optional[list[str]] = None
    relevant_log_ids: list[str] = field(default_factory=list)

@dataclass
class SafetyCheckResult:
    score: float
    category: str
    blocked: bool
    details: dict[str, Any] = field(default_factory=dict)
