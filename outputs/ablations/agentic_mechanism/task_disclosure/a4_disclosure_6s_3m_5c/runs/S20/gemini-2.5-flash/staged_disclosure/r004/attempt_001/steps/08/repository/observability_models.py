from datetime import datetime
from typing import Dict, Any, List, Optional

class LogEntry:
    """
    Represents a single log entry for ingestion into a logging service like Google Cloud Logging.
    """
    def __init__(self, message: str, severity: str = "INFO", resource_type: str = "global",
                 resource_labels: Optional[Dict[str, str]] = None,
                 timestamp: Optional[datetime] = None,
                 json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.resource_type = resource_type
        self.resource_labels = resource_labels if resource_labels is not None else {}
        self.timestamp = timestamp if timestamp is not None else datetime.utcnow()
        self.json_payload = json_payload

    def to_google_cloud_logging_entry(self) -> Dict[str, Any]:
        """
        Converts the LogEntry to a dictionary format compatible with Google Cloud Logging's
        `entries.write` method.
        """
        entry = {
            "textPayload": self.message,
            "severity": self.severity,
            "resource": {
                "type": self.resource_type,
                "labels": self.resource_labels,
            },
            "timestamp": self.timestamp.isoformat("T") + "Z",
        }
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
        return entry

class LogQueryRequest:
    """
    Represents a request to query logs from a logging service.
    """
    def __init__(self, filter_expression: str, project_id: str,
                 order_by: str = "timestamp desc", limit: int = 100):
        self.filter_expression = filter_expression
        self.project_id = project_id
        self.order_by = order_by
        self.limit = limit

class LogQueryResponse:
    """
    Represents the response from a log query.
    """
    def __init__(self, entries: List[LogEntry], next_page_token: Optional[str] = None):
        self.entries = entries
        self.next_page_token = next_page_token

def normalize_log_entry(entry_data: Dict[str, Any]) -> LogEntry:
    """
    Normalizes a dictionary representing a log entry (e.g., from a logging service API response)
    into a LogEntry object. This example assumes a structure similar to Google Cloud Logging.
    """
    message = entry_data.get("textPayload", entry_data.get("jsonPayload", {}).get("message", "N/A"))
    severity = entry_data.get("severity", "INFO")
    resource_type = entry_data.get("resource", {}).get("type", "global")
    resource_labels = entry_data.get("resource", {}).get("labels", {})
    timestamp_str = entry_data.get("timestamp")
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else None
    json_payload = entry_data.get("jsonPayload")

    return LogEntry(
        message=message,
        severity=severity,
        resource_type=resource_type,
        resource_labels=resource_labels,
        timestamp=timestamp,
        json_payload=json_payload
    )
