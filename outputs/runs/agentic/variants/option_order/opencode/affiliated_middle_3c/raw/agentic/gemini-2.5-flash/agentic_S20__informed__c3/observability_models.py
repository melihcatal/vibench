import datetime
from typing import Dict, Any, List, Optional


class StructuredLog:
    def __init__(self, message: str, severity: str = "INFO", **kwargs):
        self.message = message
        self.severity = severity
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.data = kwargs

    def to_json(self) -> Dict[str, Any]:
        log_entry = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
        log_entry.update(self.data)
        return log_entry


class CorrelatedLog:
    def __init__(
        self, correlation_id: str, message: str, severity: str = "INFO", **kwargs
    ):
        self.correlation_id = correlation_id
        self.message = message
        self.severity = severity
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.data = kwargs

    def to_json(self) -> Dict[str, Any]:
        log_entry = {
            "correlation_id": self.correlation_id,
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
        log_entry.update(self.data)
        return log_entry


class LogQuery:
    def __init__(
        self,
        project_id: str,
        filter_string: str,
        order_by: str = "timestamp desc",
        limit: int = 100,
    ):
        self.project_id = project_id
        self.filter_string = filter_string
        self.order_by = order_by
        self.limit = limit


class LogEntry:
    def __init__(
        self,
        timestamp: str,
        severity: str,
        message: str,
        resource_type: str,
        resource_labels: Dict[str, str],
        **kwargs,
    ):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.resource_type = resource_type
        self.resource_labels = resource_labels
        self.json_payload = kwargs

    @classmethod
    def from_gcp_entry(cls, entry: Dict[str, Any]):
        return cls(
            timestamp=entry.get("timestamp"),
            severity=entry.get("severity"),
            message=entry.get("textPayload")
            or entry.get("jsonPayload", {}).get("message", "N/A"),
            resource_type=entry.get("resource", {}).get("type"),
            resource_labels=entry.get("resource", {}).get("labels", {}),
            **entry.get("jsonPayload", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "json_payload": self.json_payload,
        }
