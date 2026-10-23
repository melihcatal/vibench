import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class LogEntry:
    log_name: str
    timestamp: str
    severity: str
    message: str
    json_payload: Optional[Dict[str, Any]] = None

@dataclass
class IncidentSummary:
    title: str
    description: str
    severity: str
    recommended_action: str
    related_logs: list[LogEntry]

@dataclass
class SafetyCheckResult:
    flagged: bool
    categories: Dict[str, bool]
    score: Dict[str, float]

@dataclass
class TranslatedMessage:
    original_text: str
    translated_text: str
    target_language_code: str

@dataclass
class EmbeddedMessage:
    text: str
    embedding: list[float]
