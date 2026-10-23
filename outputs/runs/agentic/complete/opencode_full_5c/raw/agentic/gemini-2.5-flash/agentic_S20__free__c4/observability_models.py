import datetime
from typing import Dict, Any, List, Optional


class LogEntry:
    def __init__(
        self,
        severity: str,
        message: str,
        resource: str,
        timestamp: datetime.datetime,
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
    ):
        self.severity = severity
        self.message = message
        self.resource = resource
        self.timestamp = timestamp
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload if json_payload is not None else {}

    def to_dict(self):
        return {
            "severity": self.severity,
            "message": self.message,
            "resource": self.resource,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
            "json_payload": self.json_payload,
        }


class LogQuery:
    def __init__(
        self, filter_string: str, order_by: str = "timestamp desc", limit: int = 100
    ):
        self.filter_string = filter_string
        self.order_by = order_by
        self.limit = limit


class IncidentSummary:
    def __init__(
        self, summary_text: str, affected_services: List[str], severity_level: str
    ):
        self.summary_text = summary_text
        self.affected_services = affected_services
        self.severity_level = severity_level


class SafetyCheckResult:
    def __init__(self, is_safe: bool, scores: Dict[str, float]):
        self.is_safe = is_safe
        self.scores = scores


class TranslatedMessage:
    def __init__(self, original_text: str, translated_text: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.target_language = target_language


class LogEmbedding:
    def __init__(self, original_text: str, embedding: List[float]):
        self.original_text = original_text
        self.embedding = embedding
