import datetime
from typing import Optional, Dict, Any

class LogEntry:
    """
    Represents a normalized log entry.
    """
    def __init__(self, message: str, severity: str, timestamp: datetime.datetime,
                 resource_type: Optional[str] = None, json_payload: Optional[Dict[str, Any]] = None,
                 text_payload: Optional[str] = None, correlation_id: Optional[str] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.resource_type = resource_type
        self.json_payload = json_payload
        self.text_payload = text_payload
        self.correlation_id = correlation_id

    @classmethod
    def from_gcp_log_entry(cls, entry):
        """
        Normalizes a Google Cloud Logging Entry object into a LogEntry.
        """
        message = ""
        json_payload = None
        text_payload = None
        correlation_id = None

        if entry.json_payload:
            json_payload = entry.json_payload
            message = json_payload.get("message", str(json_payload))
            correlation_id = json_payload.get("requestId")
        elif entry.text_payload:
            text_payload = entry.text_payload
            message = entry.text_payload
        elif entry.proto_payload:
            message = str(entry.proto_payload)

        return cls(
            message=message,
            severity=entry.severity,
            timestamp=entry.timestamp,
            resource_type=getattr(entry.resource, 'type', None),
            json_payload=json_payload,
            text_payload=text_payload,
            correlation_id=correlation_id
        )

    def to_dict(self):
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "resource_type": self.resource_type,
            "json_payload": self.json_payload,
            "text_payload": self.text_payload,
            "correlation_id": self.correlation_id,
        }

class IncidentSummary:
    """
    Represents a summary generated for incident review.
    """
    def __init__(self, title: str, summary_text: str, affected_components: list[str],
                 severity_score: int, recommended_actions: list[str]):
        self.title = title
        self.summary_text = summary_text
        self.affected_components = affected_components
        self.severity_score = severity_score
        self.recommended_actions = recommended_actions

    def to_dict(self):
        return {
            "title": self.title,
            "summary_text": self.summary_text,
            "affected_components": self.affected_components,
            "severity_score": self.severity_score,
            "recommended_actions": self.recommended_actions,
        }
