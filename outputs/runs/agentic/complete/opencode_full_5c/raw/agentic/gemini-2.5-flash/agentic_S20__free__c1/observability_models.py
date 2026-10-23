import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class LogEntry:
    severity: str
    message: str
    resource_type: str
    resource_labels: Dict[str, str]
    json_payload: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, str]] = None
    timestamp: Optional[str] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    insert_id: Optional[str] = None


@dataclasses.dataclass
class LogQueryResult:
    timestamp: str
    severity: str
    message: str
    json_payload: Optional[Dict[str, Any]] = None
    resource_type: str
    resource_labels: Dict[str, str]
    trace: Optional[str] = None
    span_id: Optional[str] = None


@dataclasses.dataclass
class IncidentSummary:
    title: str
    summary_text: str
    severity_level: str
    involved_services: List[str]
    log_samples: List[str]


@dataclasses.dataclass
class SafetyCheckResult:
    is_safe: bool
    reasons: List[str]


@dataclasses.dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    target_locale: str


@dataclasses.dataclass
class LogEmbeddingResult:
    original_message: str
    embedding_vector: List[float]
