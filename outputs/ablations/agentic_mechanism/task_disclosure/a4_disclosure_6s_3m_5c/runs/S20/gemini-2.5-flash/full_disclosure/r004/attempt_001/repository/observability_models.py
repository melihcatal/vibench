import dataclasses
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class LogEntry:
    timestamp: datetime
    severity: str
    message: str
    resource: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class LogQueryRequest:
    query_string: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = None
    order_by: Optional[str] = None

@dataclasses.dataclass
class LogQueryResponse:
    log_entries: List[LogEntry]
    next_page_token: Optional[str] = None

def normalize_log_entry(entry_data: Dict[str, Any]) -> LogEntry:
    """Normalizes a dictionary of log data into a structured LogEntry object."""
    timestamp_str = entry_data.get("timestamp")
    if isinstance(timestamp_str, str):
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    elif isinstance(timestamp_str, datetime):
        timestamp = timestamp_str
    else:
        timestamp = datetime.now() # Default to now if timestamp is missing or invalid

    return LogEntry(
        timestamp=timestamp,
        severity=entry_data.get("severity", "INFO").upper(),
        message=entry_data.get("message", "No message provided."),
        resource=entry_data.get("resource"),
        labels=entry_data.get("labels"),
        json_payload=entry_data.get("json_payload")
    )
