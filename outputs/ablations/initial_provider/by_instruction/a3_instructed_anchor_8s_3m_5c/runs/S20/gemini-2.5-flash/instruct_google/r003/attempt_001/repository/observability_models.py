from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class StructuredLogEntry:
    message: str
    severity: str = "INFO"
    
    # Cloud Logging specific fields
    resource: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class CorrelatedLogEntry:
    message: str
    correlation_id: str
    severity: str = "INFO"
    json_payload: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class LogQuery:
    filter: str
    order_by: str = "timestamp desc"
    limit: int = 100

@dataclass
class LogEntry:
    timestamp: str
    severity: str
    message: str
    resource_type: str
    resource_labels: Dict[str, str]
    json_payload: Optional[Dict[str, Any]] = None
