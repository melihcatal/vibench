from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from google.cloud import logging_v2


def normalize_log_name(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


@dataclass
class LogRecord:
    message: str
    severity: str = "INFO"
    timestamp: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_structured_payload(self) -> Dict[str, Any]:
        payload = {"message": self.message}
        payload.update(self.fields)
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.timestamp:
            payload["timestamp"] = self.timestamp
        return payload


@dataclass
class LogQuery:
    severity: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    minutes: int = 60
    limit: int = 20

    def to_filter(self) -> str:
        parts: List[str] = []
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.minutes)
        parts.append(f'timestamp >= "{cutoff.isoformat()}"')
        if self.severity:
            parts.append(f'severity >= {self.severity}')
        if self.field_name and self.field_value is not None:
            parts.append(f'jsonPayload.{normalize_log_name(self.field_name)} = "{self.field_value}"')
        return " AND ".join(parts)


@dataclass
class QueryResult:
    records: List[LogRecord]
    filter_expression: str

    def messages(self) -> List[str]:
        return [record.message for record in self.records]


@dataclass
class SafetyCheckResult:
    provider: str
    flagged: bool
    categories: Dict[str, float]
    raw_response: Dict[str, Any]


@dataclass
class TranslationResult:
    provider: str
    source_text: str
    translated_text: str
    target_language: str
    raw_response: Dict[str, Any]


@dataclass
class EmbeddingResult:
    provider: str
    text: str
    vector: List[float]
    raw_response: Dict[str, Any]


def parse_logging_entry(entry: logging_v2.entries.LogEntry) -> LogRecord:
    payload = dict(entry.payload or {})
    return LogRecord(
        message=payload.get("message", ""),
        severity=entry.severity.name if entry.severity else "DEFAULT",
        timestamp=entry.timestamp.isoformat() if entry.timestamp else None,
        labels=dict(entry.labels),
        correlation_id=payload.get("correlation_id"),
        fields=payload,
    )
