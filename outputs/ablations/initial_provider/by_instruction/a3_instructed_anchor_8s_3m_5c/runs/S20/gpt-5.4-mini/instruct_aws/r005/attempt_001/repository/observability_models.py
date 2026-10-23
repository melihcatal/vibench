from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): normalize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [normalize_value(v) for v in value]
    return str(value)


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    normalized = {str(k): normalize_value(v) for k, v in event.items()}
    normalized.setdefault("timestamp", utc_now_iso())
    return normalized


@dataclass(frozen=True)
class LogWriteRequest:
    log_group_name: str
    log_stream_name: str
    event: dict[str, Any]


@dataclass(frozen=True)
class LogQueryRequest:
    log_group_name: str
    start_time: int
    end_time: int
    filter_pattern: str = ""
    limit: int = 50


@dataclass(frozen=True)
class LogQueryResult:
    events: list[dict[str, Any]]
    next_token: str | None = None
