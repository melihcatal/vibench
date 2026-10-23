from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_timestamp(value: Any) -> str:
    if value is None:
        return utc_now_iso()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(event)
    payload["timestamp"] = normalize_timestamp(payload.get("timestamp"))
    payload.setdefault("severity", "INFO")
    return payload


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    timestamp: Optional[Any] = None
    service: Optional[str] = None
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": normalize_timestamp(self.timestamp),
        }
        if self.service is not None:
            payload["service"] = self.service
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.correlation_id is not None:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.fields)
        return normalize_event(payload)


@dataclass
class LogQuery:
    start_time: str
    end_time: str
    severity: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 50

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "limit": self.limit,
        }
        if self.severity:
            payload["severity"] = self.severity
        payload.update(self.field_filters)
        return payload


def normalize_results(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_event(item) for item in items]
