from datetime import datetime
from typing import Dict, Any, List, Optional

# Models inspired by Google Cloud Logging (formerly Stackdriver Logging)

class LogEntry:
    """Represents a single log entry."""
    def __init__(
        self,
        timestamp: datetime,
        severity: str,
        message: str,
        resource: Optional[Dict[str, Any]] = None,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        text_payload: Optional[str] = None,
        trace: Optional[str] = None,
        span_id: Optional[str] = None,
        insert_id: Optional[str] = None,
        log_name: Optional[str] = None,
    ):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.resource = resource if resource is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload
        self.text_payload = text_payload
        self.trace = trace
        self.span_id = span_id
        self.insert_id = insert_id
        self.log_name = log_name

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "timestamp": self.timestamp.isoformat() + "Z",
            "severity": self.severity,
            "message": self.message,
        }
        if self.resource:
            data["resource"] = self.resource
        if self.labels:
            data["labels"] = self.labels
        if self.json_payload:
            data["jsonPayload"] = self.json_payload
        if self.text_payload:
            data["textPayload"] = self.text_payload
        if self.trace:
            data["trace"] = self.trace
        if self.span_id:
            data["spanId"] = self.span_id
        if self.insert_id:
            data["insertId"] = self.insert_id
        if self.log_name:
            data["logName"] = self.log_name
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            severity=data["severity"],
            message=data.get("message", ""),
            resource=data.get("resource"),
            labels=data.get("labels"),
            json_payload=data.get("jsonPayload"),
            text_payload=data.get("textPayload"),
            trace=data.get("trace"),
            span_id=data.get("spanId"),
            insert_id=data.get("insertId"),
            log_name=data.get("logName"),
        )

class LogQueryRequest:
    """Represents a request to query log entries."""
    def __init__(
        self,
        filter: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        order_by: Optional[str] = None,
        page_size: int = 100,
        page_token: Optional[str] = None,
    ):
        self.filter = filter
        self.start_time = start_time
        self.end_time = end_time
        self.order_by = order_by
        self.page_size = page_size
        self.page_token = page_token

class LogQueryResponse:
    """Represents a response containing queried log entries."""
    def __init__(self, entries: List[LogEntry], next_page_token: Optional[str] = None):
        self.entries = entries
        self.next_page_token = next_page_token

class LogIngestionRequest:
    """Represents a request to ingest log entries."""
    def __init__(self, entries: List[LogEntry]):
        self.entries = entries

def normalize_log_entry(log_entry: Dict[str, Any]) -> LogEntry:
    """Normalizes a raw log entry dictionary into a LogEntry object.
    This function assumes basic fields and attempts to standardize them.
    """
    timestamp_str = log_entry.get("timestamp") or log_entry.get("time") or datetime.utcnow().isoformat() + "Z"
    severity = log_entry.get("severity", "INFO").upper()
    message = log_entry.get("message") or log_entry.get("textPayload") or log_entry.get("jsonPayload", {}).get("message", "N/A")

    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except ValueError:
        timestamp = datetime.utcnow() # Fallback to current UTC time if parsing fails

    resource = log_entry.get("resource")
    labels = log_entry.get("labels")
    json_payload = log_entry.get("jsonPayload")
    text_payload = log_entry.get("textPayload")
    trace = log_entry.get("trace")
    span_id = log_entry.get("spanId")
    insert_id = log_entry.get("insertId")
    log_name = log_entry.get("logName")

    return LogEntry(
        timestamp=timestamp,
        severity=severity,
        message=message,
        resource=resource,
        labels=labels,
        json_payload=json_payload,
        text_payload=text_payload,
        trace=trace,
        span_id=span_id,
        insert_id=insert_id,
        log_name=log_name,
    )
