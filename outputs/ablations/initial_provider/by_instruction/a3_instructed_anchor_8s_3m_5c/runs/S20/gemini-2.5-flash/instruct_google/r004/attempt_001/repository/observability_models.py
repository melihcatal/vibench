import datetime
from typing import Dict, Any, Optional, List

class StructuredLogEntry:
    def __init__(self, message: str, severity: str, timestamp: Optional[datetime.datetime] = None,
                 labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.datetime.utcnow()
        self.labels = labels if labels else {}
        self.json_payload = json_payload if json_payload else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z",
            "labels": self.labels,
            "json_payload": self.json_payload
        }

class CorrelatedLogEntry(StructuredLogEntry):
    def __init__(self, message: str, severity: str, correlation_id: str,
                 timestamp: Optional[datetime.datetime] = None,
                 labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        super().__init__(message, severity, timestamp, labels, json_payload)
        self.correlation_id = correlation_id
        self.labels['correlation_id'] = correlation_id

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict['json_payload']['correlation_id'] = self.correlation_id
        return base_dict

class LogQuery:
    def __init__(self, project_id: str, filter_string: str, order_by: str = "timestamp desc", limit: int = 100):
        self.project_id = project_id
        self.filter_string = filter_string
        self.order_by = order_by
        self.limit = limit

class LogQueryResult:
    def __init__(self, entries: List[Dict[str, Any]]):
        self.entries = entries

    def to_list(self) -> List[Dict[str, Any]]:
        return self.entries
