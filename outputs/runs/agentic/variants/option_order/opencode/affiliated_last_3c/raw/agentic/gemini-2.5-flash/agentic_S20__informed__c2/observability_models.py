import json
from datetime import datetime
from typing import Any, Dict, List, Optional


class LogEntry:
    def __init__(
        self,
        severity: str,
        message: str,
        resource_type: str = "global",
        resource_labels: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
    ):
        self.severity = severity
        self.message = message
        self.resource_type = resource_type
        self.resource_labels = resource_labels if resource_labels is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

    def to_dict(self):
        entry = {
            "severity": self.severity,
            "textPayload": self.message,
            "resource": {"type": self.resource_type, "labels": self.resource_labels},
            "labels": self.labels,
        }
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
            del entry["textPayload"]  # Structured logs use jsonPayload
        return entry


class LogQuery:
    def __init__(
        self, filter_string: str, order_by: str = "timestamp desc", page_size: int = 100
    ):
        self.filter_string = filter_string
        self.order_by = order_by
        self.page_size = page_size


class LogQueryResult:
    def __init__(self, entries: List[Dict[str, Any]]):
        self.entries = entries

    def to_json(self):
        return json.dumps(self.entries, indent=2)
