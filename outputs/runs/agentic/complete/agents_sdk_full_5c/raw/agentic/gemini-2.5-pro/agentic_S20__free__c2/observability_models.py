from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class StructuredLog:
    """Represents a structured log entry."""
    message: str
    user_id: str
    request_id: str
    http_method: str
    resource: str
    http_status: int
    latency_ms: int
    additional_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CorrelatedLog:
    """Represents a log entry with a correlation/trace ID."""
    message: str
    service_name: str
    correlation_id: str
    severity: str = "INFO"
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LogQueryResult:
    """Represents a single log entry returned from a query."""
    timestamp: str
    severity: str
    message: str
    payload: Dict[str, Any]
    trace_id: Optional[str] = None
