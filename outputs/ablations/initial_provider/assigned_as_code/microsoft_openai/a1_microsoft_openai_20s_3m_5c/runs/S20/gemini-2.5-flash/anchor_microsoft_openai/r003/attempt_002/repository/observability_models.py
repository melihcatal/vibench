from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class LogEvent:
    event_name: str
    severity: str
    message: str
    properties: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

@dataclass
class QueryParameters:
    workspace_id: str
    query: str
    timespan: Optional[str] = None # e.g., "PT1H" for 1 hour, "P1D" for 1 day
    start_time: Optional[str] = None # ISO 8601 format
    end_time: Optional[str] = None # ISO 8601 format

@dataclass
class LogQueryResponse:
    tables: list
