from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class StructuredLogEvent:
    severity: str
    message: str
    payload: Dict[str, Any]
    trace: Optional[str] = None
    span_id: Optional[str] = None
    correlation_id: Optional[str] = None
    timestamp: Optional[datetime] = None

    def to_json_payload(self) -> Dict[str, Any]:
        data = dict(self.payload)
        data["message"] = self.message
        data["severity"] = self.severity
        if self.correlation_id is not None:
            data["correlation_id"] = self.correlation_id
        if self.trace is not None:
            data["trace"] = self.trace
        if self.span_id is not None:
            data["span_id"] = self.span_id
        return data


@dataclass(frozen=True)
class LogQueryRequest:
    start_time: datetime
    end_time: datetime
    severity: Optional[str] = None
    field_filters: Optional[Mapping[str, Any]] = None
    limit: int = 50


@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    severity: str
    message: str
    payload: Dict[str, Any]


@dataclass(frozen=True)
class LogQueryResponse:
    records: List[LogRecord]


@dataclass(frozen=True)
class IncidentSummary:
    title: str
    summary: str
    error_count: int
    earliest_timestamp: Optional[datetime]
    latest_timestamp: Optional[datetime]
    top_messages: List[str]


@dataclass(frozen=True)
class SafetyCheckResult:
    is_safe: bool
    reasons: List[str]


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    embedding: List[float]


def normalize_timestamp(value: Optional[datetime]) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
