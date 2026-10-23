from typing import Literal, Optional, Dict, Any, List
from datetime import datetime

# Define common log entry structure for better local type hinting/understanding
LogSeverity = Literal["DEFAULT", "DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]

class StructuredLogEntry:
    """Represents a structured log entry as expected by the logging service."""
    def __init__self, message: str, severity: LogSeverity = "INFO", **kwargs):
        self.message = message
        self.severity = severity
        self.json_payload = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "severity": self.severity,
            **self.json_payload
        }

class CorrelatedLogEntry:
    """Represents a log entry part of a correlated request."""
    def __init__self, message: str, correlation_id: str, severity: LogSeverity = "INFO", **kwargs):
        self.message = message
        self.correlation_id = correlation_id
        self.severity = severity
        self.json_payload = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "correlation_id": self.correlation_id,
            "severity": self.severity,
            **self.json_payload
        }

class LogQueryResult:
    """Represents a single log entry returned from a query."""
    def __init__selfself, timestamp: datetime, severity: str, log_name: str, payload: Any, resource_type: Optional[str] = None, labels: Optional[Dict[str, str]] = None):
        self.timestamp = timestamp
        self.severity = severity
        self.log_name = log_name
        self.payload = payload
        self.resource_type = resource_type
        self.labels = labels if labels is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "severity": self.severity,
            "log_name": self.log_name,
            "payload": self.payload,
            "resource_type": self.resource_type,
            "labels": self.labels,
        }

