import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class LogEntry:
    def __init__(
        self,
        severity: str,
        message: str,
        resource_type: str,
        resource_labels: Dict[str, str],
        json_payload: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        trace_id: Optional[str] = None,
    ):
        self.severity = severity
        self.message = message
        self.resource_type = resource_type
        self.resource_labels = resource_labels
        self.json_payload = json_payload
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.trace_id = trace_id

    def to_dict(self):
        entry = {
            "severity": self.severity,
            "message": self.message,
            "resource": {"type": self.resource_type, "labels": self.resource_labels},
            "timestamp": self.timestamp.isoformat() + "Z",
        }
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
        if self.trace_id:
            entry["logging.googleapis.com/trace"] = self.trace_id
        return entry


class LogQueryResult:
    def __init__(self, log_entry: Dict[str, Any]):
        self.log_entry = log_entry

    @property
    def severity(self) -> str:
        return self.log_entry.get("severity", "DEFAULT")

    @property
    def message(self) -> str:
        return self.log_entry.get(
            "textPayload", self.log_entry.get("jsonPayload", {}).get("message", "N/A")
        )

    @property
    def timestamp(self) -> datetime:
        ts = self.log_entry.get("timestamp")
        return datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else datetime.min

    @property
    def trace_id(self) -> Optional[str]:
        return self.log_entry.get("trace")

    @property
    def json_payload(self) -> Optional[Dict[str, Any]]:
        return self.log_entry.get("jsonPayload")

    def __str__(self):
        return json.dumps(self.log_entry, indent=2)
