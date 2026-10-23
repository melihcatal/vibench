from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_correlation_id(value: Optional[str] = None) -> str:
    return value or str(uuid.uuid4())


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    service: str = "application"
    environment: str = "production"
    correlation_id: Optional[str] = None
    timestamp: str = field(default_factory=utc_now_iso)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_structured_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "severity": self.severity,
            "service": self.service,
            "environment": self.environment,
            "timestamp": self.timestamp,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.attributes)
        return payload


@dataclass
class QueryWindow:
    minutes: int = 15


@dataclass
class LogQueryResult:
    timestamp: str
    message: str
    severity: str
    service: Optional[str] = None
    correlation_id: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentSummaryResult:
    summary: str
    contributing_errors: List[str]
    provider_model: str


@dataclass
class SafetyCheckResult:
    flagged: bool
    category_scores: Dict[str, float]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str


@dataclass
class EmbeddingResult:
    vector: List[float]
    dimensions: int
    provider_model: str


def normalize_cloudwatch_result(item: Dict[str, Any]) -> LogQueryResult:
    message = ""
    severity = ""
    timestamp = ""
    service = None
    correlation_id = None

    for field in item.get("fields", []):
        name = field.get("field")
        value = field.get("value", "")
        if name == "@message":
            message = value
        elif name == "severity":
            severity = value
        elif name == "@timestamp":
            timestamp = value
        elif name == "service":
            service = value
        elif name == "correlation_id":
            correlation_id = value

    return LogQueryResult(
        timestamp=timestamp,
        message=message,
        severity=severity or "UNKNOWN",
        service=service,
        correlation_id=correlation_id,
        raw=item,
    )
