import datetime
from typing import Dict, Any, List, Optional

class LogEntry:
    def __init__(self, message: str, severity: str, timestamp: Optional[datetime.datetime] = None,
                 labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.utcnow()
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z",
            "labels": self.labels,
            "json_payload": self.json_payload
        }

class LogQueryResult:
    def __init__(self, entries: List[LogEntry], next_page_token: Optional[str] = None):
        self.entries = entries
        self.next_page_token = next_page_token

class IncidentSummary:
    def __init__(self, summary: str, affected_services: List[str], error_count: int):
        self.summary = summary
        self.affected_services = affected_services
        self.error_count = error_count

class SafetyCheckResult:
    def __init__(self, message: str, is_safe: bool, flagged_categories: List[str]):
        self.message = message
        self.is_safe = is_safe
        self.flagged_categories = flagged_categories

class TranslatedMessage:
    def __init__(self, original_message: str, translated_message: str, target_locale: str):
        self.original_message = original_message
        self.translated_message = translated_message
        self.target_locale = target_locale

class LogEmbedding:
    def __init__(self, message: str, embedding: List[float]):
        self.message = message
        self.embedding = embedding
