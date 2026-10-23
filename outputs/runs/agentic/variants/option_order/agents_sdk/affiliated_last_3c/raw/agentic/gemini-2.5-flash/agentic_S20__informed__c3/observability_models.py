from typing import Dict, Any, Optional
from datetime import datetime

class StructuredLogEntry:
    def __init__(self, message: str, severity: str = "INFO", component: Optional[str] = None,
                 resource: Optional[Dict[str, str]] = None, **kwargs):
        self.message = message
        self.severity = severity
        self.component = component
        self.resource = resource if resource is not None else {"type": "global"}
        self.payload = kwargs

    def to_dict(self):
        entry = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        if self.component:
            entry["component"] = self.component
        if self.resource:
            entry["resource"] = self.resource
        
        # Merge additional payload directly into the entry, avoiding a nested 'jsonPayload' for simplicity
        # Google Cloud Logging often flattens a top-level JSON object directly into jsonPayload
        final_payload = {**self.payload, **entry}
        return final_payload

class CorrelatedLogEntry:
    def __init__(self, message: str, correlation_id: str, severity: str = "INFO", **kwargs):
        self.message = message
        self.correlation_id = correlation_id
        self.severity = severity
        self.payload = kwargs

    def to_dict(self):
        entry = {
            "message": self.message,
            "correlationId": self.correlation_id,
            "severity": self.severity,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **self.payload
        }
        return entry
