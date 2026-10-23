from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple


@dataclass
class LogEvent:
    message: str
    severity: str
    timestamp: datetime
    service: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None


@dataclass
class LogQueryRequest:
    start_time: datetime
    end_time: datetime
    severity: Optional[str] = None
    query: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None


@dataclass
class LogQueryResponse:
    tables: Any
    status: Optional[str] = None


def normalize_time(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_log_event(event: LogEvent) -> Dict[str, Any]:
    payload = {
        "message": event.message,
        "severity": event.severity,
        "timestamp": normalize_time(event.timestamp),
        "service": event.service,
    }
    if event.correlation_id is not None:
        payload["correlation_id"] = event.correlation_id
    if event.request_id is not None:
        payload["request_id"] = event.request_id
    if event.fields:
        payload.update(event.fields)
    return payload


def normalize_time_range(start: datetime, end: datetime) -> Tuple[datetime, datetime]:
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)
