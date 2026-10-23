import datetime
from typing import Any, Dict, List, Optional, Literal

class ManagedLogQueryRequest:
    """
    Represents a request to query managed logs.
    """
    def __init__(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        filters: Optional[Dict[str, str]] = None,
        limit: int = 100,
        order_by: Optional[str] = None,
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.filters = filters if filters is not None else {}
        self.limit = limit
        self.order_by = order_by

class ManagedLogEntry:
    """
    Represents a single managed log entry.
    """
    def __init__(
        self,
        timestamp: datetime.datetime,
        severity: Literal["DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"],
        message: str,
        resource: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        text_payload: Optional[str] = None,
    ):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.resource = resource if resource is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload
        self.text_payload = text_payload

class ManagedLogQueryResponse:
    """
    Represents the response from a managed log query.
    """
    def __init__(
        self,
        entries: List[ManagedLogEntry],
        next_page_token: Optional[str] = None,
    ):
        self.entries = entries
        self.next_page_token = next_page_token

def normalize_log_entry(raw_log_data: Dict[str, Any]) -> ManagedLogEntry:
    """
    Normalizes a raw log entry dictionary into a ManagedLogEntry object.
    This is a placeholder for actual normalization logic that would depend on the specific log source.
    """
    timestamp_str = raw_log_data.get("timestamp")
    if timestamp_str:
        timestamp = datetime.datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    else:
        timestamp = datetime.datetime.now(datetime.timezone.utc)

    return ManagedLogEntry(
        timestamp=timestamp,
        severity=raw_log_data.get("severity", "INFO").upper(),
        message=raw_log_data.get("message", "No message provided."),
        resource=raw_log_data.get("resource"),
        labels=raw_log_data.get("labels"),
        json_payload=raw_log_data.get("json_payload"),
        text_payload=raw_log_data.get("text_payload"),
    )
