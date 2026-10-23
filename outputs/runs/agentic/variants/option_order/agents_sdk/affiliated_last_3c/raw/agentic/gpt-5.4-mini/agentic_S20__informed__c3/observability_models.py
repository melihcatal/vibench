from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


@dataclass(slots=True)
class LogEvent:
    message: str
    severity: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: str | None = None
    fields: dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity.upper(),
            "timestamp": self.timestamp.astimezone(timezone.utc).isoformat(),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.fields)
        return payload


@dataclass(slots=True)
class LogQuery:
    start_time: datetime
    end_time: datetime
    severity: str | None = None
    field_filters: dict[str, Any] = field(default_factory=dict)
    limit: int = 50

    def normalized_filters(self) -> dict[str, Any]:
        data = {
            "start_time": self.start_time.astimezone(timezone.utc).isoformat(),
            "end_time": self.end_time.astimezone(timezone.utc).isoformat(),
            "limit": self.limit,
        }
        if self.severity:
            data["severity"] = self.severity.upper()
        data.update(self.field_filters)
        return data


@dataclass(slots=True)
class QueryResult:
    items: list[dict[str, Any]]
    provider: str
    raw: Any = None


@dataclass(slots=True)
class IncidentSummary:
    title: str
    severity: str
    affected_services: list[str]
    key_findings: list[str]
    raw: Any = None


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_locale: str
    raw: Any = None


@dataclass(slots=True)
class SafetyResult:
    text: str
    unsafe: bool
    categories: list[str]
    raw: Any = None


@dataclass(slots=True)
class EmbeddingResult:
    text: str
    vector: Sequence[float]
    raw: Any = None
