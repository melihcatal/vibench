from typing import TypedDict, Dict, Any, List, Optional
from datetime import datetime

class StructuredLogEvent(TypedDict):
    message: str
    severity: str
    correlation_id: Optional[str]
    extra: Dict[str, Any]

class LogQueryParams(TypedDict):
    severity: Optional[str]
    field_filter: Optional[str]
    start_time: str  # ISO
    end_time: str    # ISO

class LogEntry(TypedDict):
    timestamp: str
    severity: str
    message: str
    payload: Dict[str, Any]