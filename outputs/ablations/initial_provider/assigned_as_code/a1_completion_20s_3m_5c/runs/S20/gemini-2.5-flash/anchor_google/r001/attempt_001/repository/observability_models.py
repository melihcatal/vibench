from typing import Dict, Any, List
from datetime import datetime

class LogEntry:
    def __init__(self, message: str, severity: str, timestamp: datetime, labels: Dict[str, str] = None, json_payload: Dict[str, Any] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

    def to_dict(self):
        entry = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.labels:
            entry["labels"] = self.labels
        if self.json_payload:
            entry["json_payload"] = self.json_payload
        return entry


class LogQueryRequest:
    def __init__(self, query_string: str, time_range_seconds: int = 3600, page_size: int = 100):
        self.query_string = query_string
        self.time_range_seconds = time_range_seconds
        self.page_size = page_size


class LogQueryResponse:
    def __init__(self, entries: List[LogEntry], next_page_token: str = None):
        self.entries = entries
        self.next_page_token = next_page_token
