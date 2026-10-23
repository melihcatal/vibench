from typing import Optional, Dict, Any
from datetime import datetime

class LogEntry:
    def __init__(self, log_name: str, payload: Dict[str, Any], severity: str = "INFO", resource_type: str = "global", resource_labels: Optional[Dict[str, str]] = None):
        self.log_name = log_name
        self.payload = payload
        self.severity = severity
        self.resource_type = resource_type
        self.resource_labels = resource_labels if resource_labels is not None else {}

class LogQueryResult:
    def __init__(self, timestamp: datetime, severity: str, message: str, full_payload: Dict[str, Any]):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.full_payload = full_payload

class SafetyAttributes:
    def __init__(self, categories: Dict[str, float], blocked: bool, safety_ratings: Any = None):
        self.categories = categories
        self.blocked = blocked
        self.safety_ratings = safety_ratings