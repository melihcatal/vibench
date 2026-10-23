from typing import Optional, Dict, Any
from datetime import datetime

class LogEntry:
    """A simple model for a structured log entry."""
    def __init__(
        self, 
        message: str,
        severity: str = "INFO",
        timestamp: Optional[datetime] = None,
        component: Optional[str] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.component = component
        self.correlation_id = correlation_id
        self.metadata = metadata if metadata is not None else {}

    def to_json_struct(self) -> Dict[str, Any]:
        """Converts the log entry to a dictionary suitable for JSON logging."""
        data = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z",
        }
        if self.component: 
            data["component"] = self.component
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        data.update(self.metadata)
        return data

    @classmethod
    def from_gcp_log_entry(cls, gcp_entry) -> 'LogEntry':
        """Creates a LogEntry from a Google Cloud Logging LogEntry object."""
        message = gcp_entry.text_payload if gcp_entry.text_payload else str(gcp_entry.json_payload)
        severity = gcp_entry.severity if gcp_entry.severity else "INFO"
        timestamp = gcp_entry.timestamp.replace(tzinfo=None) if gcp_entry.timestamp else None

        component = None
        correlation_id = None
        metadata = {}

        if gcp_entry.json_payload:
            if "component" in gcp_entry.json_payload: 
                component = gcp_entry.json_payload["component"]
            if "correlation_id" in gcp_entry.json_payload:
                correlation_id = gcp_entry.json_payload["correlation_id"]
            # Copy other top-level fields to metadata, excluding ones already extracted
            for key, value in gcp_entry.json_payload.items():
                if key not in ["message", "severity", "component", "correlation_id"]:
                    metadata[key] = value

        return cls(
            message=message,
            severity=severity,
            timestamp=timestamp,
            component=component,
            correlation_id=correlation_id,
            metadata=metadata
        )
