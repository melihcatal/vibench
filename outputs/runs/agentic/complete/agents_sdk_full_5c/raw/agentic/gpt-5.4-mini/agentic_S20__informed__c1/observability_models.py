from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class LogEvent:
    message: str
    service: str
    level: str = "info"
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)


def normalize_timestamp(value: Optional[datetime]) -> str:
    ts = value or datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_log_event(event: LogEvent) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "message": event.message,
        "service": event.service,
        "status": event.level,
        "timestamp": normalize_timestamp(event.timestamp),
    }
    if event.correlation_id:
        payload["correlation_id"] = event.correlation_id
    if event.request_id:
        payload["request_id"] = event.request_id
    payload.update(event.fields)
    return payload


def coerce_events(response: Mapping[str, Any]) -> List[Dict[str, Any]]:
    data = response.get("data", [])
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []
