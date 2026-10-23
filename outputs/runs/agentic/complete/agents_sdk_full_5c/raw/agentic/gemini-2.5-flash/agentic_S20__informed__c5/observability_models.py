from typing import Dict, Any, Optional
from datetime import datetime

class LogEntry:
    """
    A simple model to represent a normalized log entry.
    """
    def __init__(
        self,
        message: str,
        severity: str,
        timestamp: datetime,
        log_name: str,
        resource: Optional[Dict[str, Any]] = None,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        text_payload: Optional[str] = None,
        correlation_id: Optional[str] = None,
        **kwargs
    ):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.log_name = log_name
        self.resource = resource if resource is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}
        self.text_payload = text_payload
        self.correlation_id = correlation_id
        self.extra_fields = kwargs

    @classmethod
    def from_gcp_log_entry(cls, gcp_entry) -> 'LogEntry':
        """
        Normalizes a google.cloud.logging.entries.LogEntry object into a LogEntry.
        """
        message = ""
        json_payload = {}
        text_payload = None

        if gcp_entry.payload and isinstance(gcp_entry.payload, dict):
            json_payload = gcp_entry.payload
            message = json_payload.get("message", json.dumps(json_payload))
            correlation_id = json_payload.get("correlation_id")
        elif gcp_entry.payload and isinstance(gcp_entry.payload, str):
            text_payload = gcp_entry.payload
            message = text_payload
            correlation_id = None # Assuming correlation_id is for structured logs
        else:
            message = str(gcp_entry.payload) if gcp_entry.payload is not None else "(No payload)"
            correlation_id = None

        return cls(
            message=message,
            severity=gcp_entry.severity,
            timestamp=gcp_entry.timestamp,
            log_name=gcp_entry.log_name,
            resource=gcp_entry.resource.labels if gcp_entry.resource else None,
            labels=gcp_entry.labels,
            json_payload=json_payload,
            text_payload=text_payload,
            correlation_id=correlation_id
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts the log entry to a dictionary."""
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "log_name": self.log_name,
            "resource": self.resource,
            "labels": self.labels,
            "json_payload": self.json_payload,
            "text_payload": self.text_payload,
            "correlation_id": self.correlation_id,
            "extra_fields": self.extra_fields
        }

if __name__ == "__main__":
    import json
    # Example usage
    now = datetime.now()
    log_entry_data = LogEntry(
        message="Service started successfully",
        severity="INFO",
        timestamp=now,
        log_name="my-service-logs",
        json_payload={"service": "frontend", "version": "1.0.0"},
        correlation_id="startup-001"
    )
    print("Normalized LogEntry:")
    print(json.dumps(log_entry_data.to_dict(), indent=2))
