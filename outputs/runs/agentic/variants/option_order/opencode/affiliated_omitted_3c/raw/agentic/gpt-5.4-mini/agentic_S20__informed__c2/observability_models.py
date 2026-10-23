import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _iso_from(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(fields or {})


def normalize_severity(severity: Optional[str]) -> str:
    return (severity or "info").strip().lower()


def normalize_message(message: str) -> str:
    return str(message).strip()


def log_event_body(
    service: str,
    message: str,
    severity: str = "info",
    correlation_id: Optional[str] = None,
    fields: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = {
        "service": service,
        "message": normalize_message(message),
        "severity": normalize_severity(severity),
        "timestamp": _iso_now(),
        "fields": normalize_fields(fields),
    }
    if correlation_id:
        payload["correlation_id"] = correlation_id
    return payload


def query_window(
    start_time: Optional[str] = None, end_time: Optional[str] = None, minutes: int = 15
) -> Dict[str, str]:
    end = _iso_from(end_time) or _iso_now()
    if start_time:
        start = _iso_from(start_time)
    else:
        start_dt = datetime.now(timezone.utc).timestamp() - (minutes * 60)
        start = datetime.fromtimestamp(start_dt, tz=timezone.utc).isoformat()
    return {"start_time": start, "end_time": end}


def response_records(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("records", "results", "events", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [r for r in value if isinstance(r, dict)]
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    return []


@dataclass
class LogQuery:
    text: Optional[str] = None
    severity: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class LogWriteRequest:
    message: str
    severity: str = "info"
    correlation_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
