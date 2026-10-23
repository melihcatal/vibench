import datetime
from typing import Dict, Any, List, Optional


class LogEntry:
    def __init__(
        self,
        message: str,
        severity: str,
        timestamp: datetime.datetime,
        resource: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        trace: Optional[str] = None,
    ):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.resource = resource if resource is not None else {}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload
        self.trace = trace

    def to_dict(self):
        entry = {
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z",
            "resource": self.resource,
            "labels": self.labels,
        }
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
        else:
            entry["textPayload"] = self.message
        if self.trace:
            entry["trace"] = self.trace
        return entry


class LogQueryResult:
    def __init__(self, entries: List[LogEntry], next_page_token: Optional[str] = None):
        self.entries = entries
        self.next_page_token = next_page_token


class IncidentSummary:
    def __init__(self, summary_text: str, critical_errors: int, error_rate: float):
        self.summary_text = summary_text
        self.critical_errors = critical_errors
        self.error_rate = error_rate
