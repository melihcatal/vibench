import datetime
from typing import Dict, Any, List, Optional

class StructuredLogEntry:
    def __init__(self, message: str, severity: str = "INFO", resource_type: str = "global", labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.resource_type = resource_type
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

class CorrelatedLogEntry:
    def __init__(self, message: str, correlation_id: str, severity: str = "INFO", labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.correlation_id = correlation_id
        self.severity = severity
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

class LogQueryParameters:
    def __init__(self, filter_string: str, start_time: Optional[datetime.datetime] = None, end_time: Optional[datetime.datetime] = None, limit: int = 100):
        self.filter_string = filter_string
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit

class LogEntry:
    def __init__(self, text_payload: Optional[str] = None, json_payload: Optional[Dict[str, Any]] = None, severity: str = "INFO", timestamp: Optional[datetime.datetime] = None, labels: Optional[Dict[str, str]] = None, log_name: Optional[str] = None):
        self.text_payload = text_payload
        self.json_payload = json_payload
        self.severity = severity
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now(datetime.timezone.utc)
        self.labels = labels if labels is not None else {}
        self.log_name = log_name

class LogQueryResult:
    def __init__(self, entries: List[LogEntry], next_page_token: Optional[str] = None):
        self.entries = entries
        self.next_page_token = next_page_token
