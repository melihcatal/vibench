import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class LogEntry:
    message: str
    severity: str
    timestamp: str
    resource_id: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class StructuredLogEntry(LogEntry):
    # Additional fields specific to structured logs, if any
    pass

@dataclasses.dataclass
class CorrelatedLogEntry(LogEntry):
    correlation_id: str
    # Additional fields specific to correlated logs, if any
    pass
