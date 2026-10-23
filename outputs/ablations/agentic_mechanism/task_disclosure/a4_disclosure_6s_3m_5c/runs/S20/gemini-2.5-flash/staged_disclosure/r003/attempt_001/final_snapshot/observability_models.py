from datetime import datetime
from typing import Dict, Any, List, Optional

class LogEntry:
    """Represents a single log entry."""
    def __init__(self, timestamp: datetime, message: str, severity: str = "INFO", resource: Optional[Dict[str, str]] = None, labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.message = message
        self.severity = severity
        self.resource = resource if resource is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload

    def to_json(self) -> Dict[str, Any]:
        payload = {
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "severity": self.severity,
            "resource": self.resource,
            "labels": self.labels,
        }
        if self.json_payload:
            payload["json_payload"] = self.json_payload
        return payload

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> "LogEntry":
        return LogEntry(
            timestamp=datetime.fromisoformat(json_data["timestamp"]),
            message=json_data["message"],
            severity=json_data.get("severity", "INFO"),
            resource=json_data.get("resource"),
            labels=json_data.get("labels"),
            json_payload=json_data.get("json_payload")
        )

class LogIngestionRequest:
    """Represents a request to ingest logs."""
    def __init__(self, entries: List[LogEntry], common_resource: Optional[Dict[str, str]] = None, common_labels: Optional[Dict[str, str]] = None):
        self.entries = entries
        self.common_resource = common_resource
        self.common_labels = common_labels

    def to_json(self) -> Dict[str, Any]:
        data = {
            "entries": [entry.to_json() for entry in self.entries]
        }
        if self.common_resource:
            data["common_resource"] = self.common_resource
        if self.common_labels:
            data["common_labels"] = self.common_labels
        return data

class LogIngestionResponse:
    """Represents a response from a log ingestion request."""
    def __init__(self, success: bool, ingested_count: int = 0, errors: Optional[List[str]] = None):
        self.success = success
        self.ingested_count = ingested_count
        self.errors = errors if errors is not None else []

    def to_json(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "ingested_count": self.ingested_count,
            "errors": self.errors
        }

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> "LogIngestionResponse":
        return LogIngestionResponse(
            success=json_data["success"],
            ingested_count=json_data.get("ingested_count", 0),
            errors=json_data.get("errors")
        )

class LogQueryRequest:
    """Represents a request to query logs."""
    def __init__(self, query_string: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, limit: int = 100):
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit

    def to_json(self) -> Dict[str, Any]:
        data = {
            "query_string": self.query_string,
            "limit": self.limit,
        }
        if self.start_time:
            data["start_time"] = self.start_time.isoformat()
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
        return data

class LogQueryResponse:
    """Represents a response from a log query request."""
    def __init__(self, entries: List[LogEntry], total_results: int = 0, next_page_token: Optional[str] = None):
        self.entries = entries
        self.total_results = total_results
        self.next_page_token = next_page_token

    def to_json(self) -> Dict[str, Any]:
        return {
            "entries": [entry.to_json() for entry in self.entries],
            "total_results": self.total_results,
            "next_page_token": self.next_page_token
        }

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> "LogQueryResponse":
        return LogQueryResponse(
            entries=[LogEntry.from_json(entry_data) for entry_data in json_data.get("entries", [])],
            total_results=json_data.get("total_results", 0),
            next_page_token=json_data.get("next_page_token")
        )

def normalize_log_entry(log_data: Dict[str, Any]) -> LogEntry:
    """Normalizes raw log data into a structured LogEntry."""
    timestamp_str = log_data.get("timestamp") or datetime.utcnow().isoformat()
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) # Handle 'Z' for UTC
    except ValueError:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ") # Common AWS format
    
    message = log_data.get("message", "No message provided")
    severity = log_data.get("severity", "INFO").upper()

    resource = log_data.get("resource", {})
    labels = log_data.get("labels", {})
    json_payload = log_data.get("json_payload")

    # Attempt to extract common fields if they are in the root and not already in resource/labels
    for key in ["service_name", "host", "pod_name", "container_name"]:
        if key in log_data and key not in resource:
            resource[key] = log_data[key]
    
    for key in ["trace_id", "span_id", "session_id"]:
        if key in log_data and key not in labels:
            labels[key] = log_data[key]

    # If the original log_data has extra fields, put them into json_payload
    if not json_payload:
        json_payload = {k: v for k, v in log_data.items() if k not in ["timestamp", "message", "severity", "resource", "labels", "json_payload"]}
        if not json_payload: # If after filtering there's nothing left, set to None
            json_payload = None

    return LogEntry(
        timestamp=timestamp,
        message=message,
        severity=severity,
        resource=resource,
        labels=labels,
        json_payload=json_payload
    )

def denormalize_log_entry(log_entry: LogEntry) -> Dict[str, Any]:
    """Denormalizes a LogEntry back into a dictionary for external systems."""
    return log_entry.to_json()
