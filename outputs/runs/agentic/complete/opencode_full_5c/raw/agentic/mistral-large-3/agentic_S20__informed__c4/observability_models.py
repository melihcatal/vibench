from typing import Dict, Any, List, Optional
from datetime import datetime


class LogEntry:
    """Represents a normalized log entry for Google Cloud Logging."""

    def __init__(
        self,
        severity: str = "INFO",
        message: str = "",
        timestamp: Optional[str] = None,
        json_payload: Optional[Dict[str, Any]] = None,
    ):
        self.severity = severity.upper()
        self.message = message
        self.timestamp = timestamp or datetime.utcnow().isoformat() + "Z"
        self.json_payload = json_payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the log entry to a dictionary for Google Cloud Logging."""
        return {
            "severity": self.severity,
            "message": self.message,
            "timestamp": self.timestamp,
            "jsonPayload": self.json_payload,
        }


class LogQueryResponse:
    """Represents a response from a log query in Google Cloud Logging."""

    def __init__(self, entries: List[Dict[str, Any]]):
        self.entries = entries

    def get_entries(self) -> List[Dict[str, Any]]:
        """Return the log entries."""
        return self.entries
