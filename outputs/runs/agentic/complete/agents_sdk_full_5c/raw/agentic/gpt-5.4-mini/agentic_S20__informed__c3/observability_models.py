from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_severity(severity: str) -> str:
    return (severity or "INFO").strip().upper()


def normalize_log_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    normalized.setdefault("timestamp", utc_now_iso())
    if "severity" in normalized:
        normalized["severity"] = normalize_severity(str(normalized["severity"]))
    return normalized


@dataclass(frozen=True)
class LogEvent:
    service: str
    severity: str
    message: str
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: str | None = None
    fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = {
            "service": self.service,
            "severity": normalize_severity(self.severity),
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        data.update(self.fields)
        return normalize_log_payload(data)


@dataclass(frozen=True)
class LogQuery:
    start_time: str
    end_time: str
    severity: str | None = None
    field_filters: dict[str, Any] = field(default_factory=dict)
    limit: int = 100


@dataclass(frozen=True)
class LogQueryResult:
    entries: list[dict[str, Any]]
    raw_response: Any | None = None


@dataclass(frozen=True)
class SafetyCheckResult:
    unsafe: bool
    categories: list[str]
    raw_response: Any | None = None


@dataclass(frozen=True)
class TranslationResult:
    text: str
    target_locale: str
    raw_response: Any | None = None


@dataclass(frozen=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    raw_response: Any | None = None


@dataclass(frozen=True)
class IncidentSummary:
    summary: str
    key_findings: list[str]
    raw_response: Any | None = None
