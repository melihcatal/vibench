from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


def _iso_utc(value: datetime | None) -> str:
    if value is None:
        value = datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_severity(value: Any) -> str:
    text = normalize_text(value).upper()
    return text if text else "INFO"


def normalize_event(payload: Mapping[str, Any]) -> dict[str, Any]:
    event = dict(payload)
    event["timestamp"] = _iso_utc(event.get("timestamp") if isinstance(event.get("timestamp"), datetime) else None)
    event["severity"] = normalize_severity(event.get("severity"))
    event["message"] = normalize_text(event.get("message"))
    if event.get("correlation_id") is not None:
        event["correlation_id"] = normalize_text(event.get("correlation_id"))
    if event.get("service_name") is not None:
        event["service_name"] = normalize_text(event.get("service_name"))
    return event


@dataclass(frozen=True)
class LogQueryWindow:
    start_time: str
    end_time: str


@dataclass(frozen=True)
class LogWriteResult:
    status: str
    resource_id: str | None = None
    request_id: str | None = None
    raw: Any = None


@dataclass(frozen=True)
class LogQueryResult:
    items: list[dict[str, Any]]
    raw: Any = None
