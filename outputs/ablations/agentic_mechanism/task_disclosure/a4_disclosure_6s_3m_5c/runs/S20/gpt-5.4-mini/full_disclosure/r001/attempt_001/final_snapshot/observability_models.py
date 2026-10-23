from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional


def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_timestamp(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, datetime):
        return _ensure_utc(value).isoformat().replace("+00:00", "Z")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return _ensure_utc(parsed).isoformat().replace("+00:00", "Z")
    return normalize_timestamp(str(value))


def normalize_fields(fields: Optional[Mapping[str, Any]] = None, **extra: Any) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    if fields:
        normalized.update(dict(fields))
    if extra:
        normalized.update(extra)
    return normalized


def normalize_log_record(record: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(record)
    for key in ("timestamp", "time", "created_at", "occurred_at"):
        if key in data and data[key] is not None:
            data[key] = normalize_timestamp(data[key])
    if "severity" in data and data["severity"] is not None:
        data["severity"] = str(data["severity"]).lower()
    if "level" in data and data["level"] is not None:
        data["level"] = str(data["level"]).lower()
    if "fields" in data and isinstance(data["fields"], Mapping):
        data["fields"] = normalize_fields(data["fields"])
    return data


@dataclass(frozen=True)
class LogQueryRequest:
    query: str
    start_time: datetime
    end_time: datetime
    limit: int = 100
    field_name: Optional[str] = None
    field_value: Optional[str] = None

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "filter": {
                "from": normalize_timestamp(self.start_time),
                "to": normalize_timestamp(self.end_time),
                "query": self.query,
            },
            "page": {"limit": self.limit},
        }
        return payload


@dataclass(frozen=True)
class LogIngestionEvent:
    message: str
    severity: str = "info"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fields: MutableMapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": normalize_timestamp(self.timestamp),
        }
        payload.update(normalize_fields(self.fields))
        return payload


@dataclass(frozen=True)
class LogQueryResponse:
    data: list[dict[str, Any]]
    raw: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_api_response(cls, response: Mapping[str, Any]) -> "LogQueryResponse":
        items = response.get("data", response)
        if isinstance(items, Mapping):
            normalized_items = [normalize_log_record(items)]
        else:
            normalized_items = [normalize_log_record(item) for item in items]
        return cls(data=normalized_items, raw=dict(response))


@dataclass(frozen=True)
class IngestionResponse:
    status_code: int
    request_id: Optional[str] = None
    raw: Optional[Mapping[str, Any]] = None

    @classmethod
    def from_http_response(cls, status_code: int, payload: Optional[Mapping[str, Any]] = None) -> "IngestionResponse":
        request_id = None
        if payload and isinstance(payload, Mapping):
            request_id = payload.get("request_id") or payload.get("id")
        return cls(status_code=status_code, request_id=request_id, raw=dict(payload) if payload else None)
