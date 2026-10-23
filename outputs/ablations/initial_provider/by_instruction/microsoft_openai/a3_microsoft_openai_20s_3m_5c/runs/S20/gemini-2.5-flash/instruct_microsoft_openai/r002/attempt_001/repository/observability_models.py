import json
from datetime import datetime
from typing import Dict, Any, List, Optional

class LogEvent:
    def __init__(self, message: str, severity: str, properties: Optional[Dict[str, Any]] = None, timestamp: Optional[datetime] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.properties = properties if properties else {}

    def to_json(self) -> str:
        data = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }
        data.update(self.properties)
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        message = data.pop("message")
        severity = data.pop("severity")
        timestamp_str = data.pop("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str)
        return cls(message=message, severity=severity, properties=data, timestamp=timestamp)

class LogQuery:
    def __init__(self, query_string: str, time_range_start: datetime, time_range_end: datetime):
        self.query_string = query_string
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end

class LogQueryResult:
    def __init__(self, logs: List[LogEvent]):
        self.logs = logs

class IncidentSummary:
    def __init__(self, summary_text: str, severity_level: str, affected_services: List[str]):
        self.summary_text = summary_text
        self.severity_level = severity_level
        self.affected_services = affected_services

class SafetyCheckResult:
    def __init__(self, is_safe: bool, flagged_categories: List[str], moderation_score: Dict[str, float]):
        self.is_safe = is_safe
        self.flagged_categories = flagged_categories
        self.moderation_score = moderation_score

class TranslatedMessage:
    def __init__(self, original_text: str, translated_text: str, target_language: str):
        self.original_text = original_text
        self.translated_text = translated_text
        self.target_language = target_language

class EmbeddedMessage:
    def __init__(self, original_text: str, embedding: List[float]):
        self.original_text = original_text
        self.embedding = embedding
