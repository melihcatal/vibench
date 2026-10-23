from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def _coerce_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)
    raise TypeError(f"Unsupported datetime value: {value!r}")


def _normalize_timestamp(value: Any) -> str:
    return _coerce_datetime(value).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_value(v) for v in value]
    if isinstance(value, datetime):
        return _normalize_timestamp(value)
    return value


@dataclass(frozen=True)
class LogQueryRequest:
    query: str
    start_time: datetime | str | int | float | None = None
    end_time: datetime | str | int | float | None = None
    filters: Mapping[str, Any] = field(default_factory=dict)
    limit: int | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"query": self.query}
        if self.start_time is not None:
            payload["start_time"] = _normalize_timestamp(self.start_time)
        if self.end_time is not None:
            payload["end_time"] = _normalize_timestamp(self.end_time)
        if self.filters:
            payload["filters"] = _normalize_value(dict(self.filters))
        if self.limit is not None:
            payload["limit"] = int(self.limit)
        return payload


@dataclass(frozen=True)
class LogIngestRequest:
    message: str
    severity: str | None = None
    timestamp: datetime | str | int | float | None = None
    fields: Mapping[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"message": self.message}
        if self.severity is not None:
            payload["severity"] = self.severity
        if self.timestamp is not None:
            payload["timestamp"] = _normalize_timestamp(self.timestamp)
        if self.fields:
            payload["fields"] = _normalize_value(dict(self.fields))
        if self.correlation_id is not None:
            payload["correlation_id"] = self.correlation_id
        return payload


@dataclass(frozen=True)
class LogRecord:
    message: str
    timestamp: datetime
    severity: str | None = None
    fields: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LogRecord":
        message = str(data.get("message", ""))
        timestamp = _coerce_datetime(data.get("timestamp", datetime.now(timezone.utc)))
        severity = data.get("severity")
        correlation_id = data.get("correlation_id") or data.get("correlationId")
        fields = data.get("fields")
        if not isinstance(fields, Mapping):
            fields = {k: v for k, v in data.items() if k not in {"message", "timestamp", "severity", "correlation_id", "correlationId", "fields"}}
        return cls(
            message=message,
            timestamp=timestamp,
            severity=str(severity) if severity is not None else None,
            fields={str(k): _normalize_value(v) for k, v in dict(fields).items()},
            correlation_id=str(correlation_id) if correlation_id is not None else None,
            raw={str(k): _normalize_value(v) for k, v in dict(data).items()},
        )

    def to_mapping(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "message": self.message,
            "timestamp": _normalize_timestamp(self.timestamp),
            "fields": _normalize_value(self.fields),
        }
        if self.severity is not None:
            payload["severity"] = self.severity
        if self.correlation_id is not None:
            payload["correlation_id"] = self.correlation_id
        return payload


@dataclass(frozen=True)
class LogQueryResponse:
    records: list[LogRecord]
    next_token: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LogQueryResponse":
        items = data.get("records") or data.get("results") or data.get("logs") or []
        if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
            items = []
        records = [LogRecord.from_mapping(item) for item in items if isinstance(item, Mapping)]
        next_token = data.get("next_token") or data.get("nextToken")
        return cls(records=records, next_token=str(next_token) if next_token is not None else None, raw={str(k): _normalize_value(v) for k, v in dict(data).items()})


@dataclass(frozen=True)
class LogIngestResponse:
    accepted: bool
    record: LogRecord | None = None
    request_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LogIngestResponse":
        record_data = data.get("record")
        record = LogRecord.from_mapping(record_data) if isinstance(record_data, Mapping) else None
        accepted = bool(data.get("accepted", data.get("success", True)))
        request_id = data.get("request_id") or data.get("requestId")
        return cls(accepted=accepted, record=record, request_id=str(request_id) if request_id is not None else None, raw={str(k): _normalize_value(v) for k, v in dict(data).items()})
