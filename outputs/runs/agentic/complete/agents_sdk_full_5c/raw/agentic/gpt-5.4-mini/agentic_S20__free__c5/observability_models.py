from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    timestamp: Optional[str] = None
    service: str = "app"
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryFilters:
    severity: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    since_iso: Optional[str] = None
    until_iso: Optional[str] = None
    limit: int = 50


@dataclass
class IncidentSummaryRequest:
    severity: str
    time_window_minutes: int
    findings: List[str]


@dataclass
class SafetyCheckRequest:
    message: str


@dataclass
class TranslationRequest:
    message: str
    target_locale: str


@dataclass
class EmbeddingRequest:
    messages: List[str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_log_event(event: LogEvent) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "message": event.message,
        "severity": event.severity,
        "timestamp": event.timestamp or utc_now_iso(),
        "service": event.service,
        "fields": dict(event.fields),
    }
    if event.request_id is not None:
        payload["request_id"] = event.request_id
    if event.correlation_id is not None:
        payload["correlation_id"] = event.correlation_id
    return payload


def normalize_query_filters(filters: QueryFilters) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"limit": filters.limit}
    if filters.severity:
        payload["severity"] = filters.severity
    if filters.field_name is not None:
        payload["field_name"] = filters.field_name
    if filters.field_value is not None:
        payload["field_value"] = filters.field_value
    if filters.since_iso is not None:
        payload["since"] = filters.since_iso
    if filters.until_iso is not None:
        payload["until"] = filters.until_iso
    return payload
