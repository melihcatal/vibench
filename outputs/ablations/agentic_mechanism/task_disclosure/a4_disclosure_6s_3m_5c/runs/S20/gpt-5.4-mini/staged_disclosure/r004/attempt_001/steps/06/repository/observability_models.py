from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional


def _to_utc_iso(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping)
 and not isinstance(value, dict):
        return dict(value)
    if isinstance(value, dict):
        return value
    raise TypeError("expected mapping")


@dataclass(frozen=True)
class LogQueryRequest:
    query: str
    start_time: str | datetime | int | float | None = None
    end_time: str | datetime | int | float | None = None
    limit: int = 100
    cursor: str | None = None
    filters: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload = {"query": self.query, "limit": self.limit}
        if self.start_time is not None:
            payload["start_time"] = _to_utc_iso(self.start_time)
        if self.end_time is not None:
            payload["end_time"] = _to_utc_iso(self.end_time)
        if self.cursor is not None:
            payload["cursor"] = self.cursor
        if self.filters:
            payload["filters"] = dict(self.filters)
        return payload


@dataclass(frozen=True)
class LogQueryResponse:
    results: list[dict[str, Any]]
    next_cursor: str | None = None
    total_count: int | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "LogQueryResponse":
        data = _coerce_mapping(payload)
        results = list(data.get("results") or data.get("items") or [])
        next_cursor = data.get("next_cursor") or data.get("cursor")
        total_count = data.get("total_count")
        return cls(results=results, next_cursor=next_cursor, total_count=total_count, raw=data)


@dataclass(frozen=True)
class LogIngestionRecord:
    message: str
    timestamp: str | datetime | int | float | None = None
    level: str | None = None
    service: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def normalize(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"message": self.message}
        payload["timestamp"] = _to_utc_iso(self.timestamp)
        if self.level is not None:
            payload["level"] = self.level
        if self.service is not None:
            payload["service"] = self.service
        if self.trace_id is not None:
            payload["trace_id"] = self.trace_id
        if self.span_id is not None:
            payload["span_id"] = self.span_id
        if self.attributes:
            payload["attributes"] = dict(self.attributes)
        return payload


@dataclass(frozen=True)
class LogIngestionRequest:
    records: list[LogIngestionRecord]
    source: str | None = None
    tags: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"records": [record.normalize() for record in self.records]}
        if self.source is not None:
            payload["source"] = self.source
        if self.tags:
            payload["tags"] = dict(self.tags)
        return payload


@dataclass(frozen=True)
class LogIngestionResponse:
    accepted: int
    rejected: int = 0
    request_id: str | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "LogIngestionResponse":
        data = _coerce_mapping(payload)
        return cls(
            accepted=int(data.get("accepted", data.get("ingested", 0))),
            rejected=int(data.get("rejected", data.get("failed", 0))),
            request_id=data.get("request_id") or data.get("id"),
            raw=data,
        )


def normalize_query_result(item: Mapping[str, Any]) -> dict[str, Any]:
    data = _coerce_mapping(item)
    normalized = dict(data)
    if "timestamp" in normalized:
        normalized["timestamp"] = _to_utc_iso(normalized["timestamp"])
    return normalized


def normalize_ingestion_record(item: Mapping[str, Any]) -> dict[str, Any]:
    data = _coerce_mapping(item)
    record = dict(data)
    if "timestamp" in record:
        record["timestamp"] = _to_utc_iso(record["timestamp"])
    elif "ts" in record:
        record["timestamp"] = _to_utc_iso(record.pop("ts"))
    return record
