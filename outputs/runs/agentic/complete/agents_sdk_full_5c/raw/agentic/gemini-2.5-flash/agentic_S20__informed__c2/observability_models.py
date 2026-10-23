import datetime
from typing import Dict, Any, Optional

class LogEntry:
    def __init__(self, message: str, severity: str = "INFO", labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

    def to_dict(self):
        entry = {
            "message": self.message,
            "severity": self.severity,
            "labels": self.labels,
        }
        if self.json_payload:
            entry["json_payload"] = self.json_payload
        return entry

class LogQueryParams:
    def __init__(self, project_id: str, filter_str: str, order_by: str = "timestamp desc", limit: int = 100):
        self.project_id = project_id
        self.filter_str = filter_str
        self.order_by = order_by
        self.limit = limit
