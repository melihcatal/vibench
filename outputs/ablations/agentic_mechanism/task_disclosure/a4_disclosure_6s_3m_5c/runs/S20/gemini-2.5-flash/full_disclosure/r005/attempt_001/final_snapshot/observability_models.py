import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class LogQueryRequest:
    filter: Optional[str] = None
    time_range: Optional[str] = None
    limit: Optional[int] = None

@dataclasses.dataclass
class LogEntry:
    timestamp: str
    severity: str
    message: str
    resource: Dict[str, Any]
    labels: Dict[str, str]
    json_payload: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class LogQueryResponse:
    entries: List[LogEntry]
    next_page_token: Optional[str] = None

def normalize_log_entry(entry: Dict[str, Any]) -> LogEntry:
    # This is a placeholder for actual normalization logic
    # In a real scenario, this would parse and validate the incoming log entry
    # and map it to the LogEntry dataclass.
    return LogEntry(
        timestamp=entry.get("timestamp", ""),
        severity=entry.get("severity", "DEFAULT"),
        message=entry.get("textPayload", entry.get("jsonPayload", {}).get("message", "")),
        resource=entry.get("resource", {}),
        labels=entry.get("labels", {}),
        json_payload=entry.get("jsonPayload")
    )

@dataclasses.dataclass
class LogIngestionRequest:
    entries: List[LogEntry]
