from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_iso8601(value: Any) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_log_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in fields.items():
        if value is None:
            continue
        if isinstance(value, datetime):
            normalized[key] = ensure_iso8601(value)
        else:
            normalized[key] = value
    return normalized


@dataclass
class LogEvent:
    message: str
    severity: str = "info"
    service: str = "app"
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "severity": self.severity,
            "service": self.service,
            "timestamp": self.timestamp or utc_now_iso(),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.fields:
            payload.update(normalize_log_fields(self.fields))
        return payload


@dataclass
class LogQuery:
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = 50

    def to_datadog_query(self) -> str:
        parts: List[str] = []
        if self.severity:
            parts.append(f"severity:{self.severity}")
        if self.field_filters:
            for key, value in self.field_filters.items():
                parts.append(f'{key}:{value}')
        return " ".join(parts) if parts else "*"


@dataclass
class LogResponse:
    results: List[Dict[str, Any]]
    raw: Any = None

    @classmethod
    def from_datadog(cls, payload: Dict[str, Any]) -> "LogResponse":
        results = payload.get("data") or payload.get("results") or []
        normalized = [normalize_log_fields(item) for item in results]
        return cls(results=normalized, raw=payload)
