from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional
from uuid import uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_mapping(value: Any) -> MutableMapping[str, Any]:
    if value is None:
        return {}
    if isinstance(value, MutableMapping):
        return dict(value)
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("expected mapping-like object")


def _normalize_timestamp(value: Any) -> str:
    if value is None:
        return _utc_now().isoformat()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    raise TypeError("unsupported timestamp value")


@dataclass(frozen=True)
class LogQueryRequest:
    query: str
    start_time: Optional[Any] = None
    end_time: Optional[Any] = None
    limit: int = 1000
    cursor: Optional[str] = None
    filters: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"query": self.query, "limit": self.limit}
        if self.start_time is not None:
            payload["start_time"] = _normalize_timestamp(self.start_time)
        if self.end_time is not None:
            payload["end_time"] = _normalize_timestamp(self.end_time)
        if self.cursor is not None:
            payload["cursor"] = self.cursor
        if self.filters:
            payload["filters"] = dict(self.filters)
        return payload


@dataclass(frozen=True)
class LogQueryResponse:
    records: list[dict[str, Any]]
    next_cursor: Optional[str] = None
    request_id: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Any) -> "LogQueryResponse":
        data = _ensure_mapping(payload)
        records = list(data.get("records") or data.get("items") or [])
        return cls(
            records=records,
            next_cursor=data.get("next_cursor") or data.get("cursor"),
            request_id=data.get("request_id") or data.get("id") or data.get("trace_id"),
            raw=data,
        )


@dataclass(frozen=True)
class LogIngestionRecord:
    message: str
    timestamp: Any = None
    level: str = "info"
    source: Optional[str] = None
    service: Optional[str] = None
    labels: Mapping[str, Any] = field(default_factory=dict)
    attributes: Mapping[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    event_id: Optional[str] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "message": self.message,
            "timestamp": _normalize_timestamp(self.timestamp),
            "level": self.level,
            "labels": dict(self.labels),
            "attributes": dict(self.attributes),
        }
        if self.source is not None:
            payload["source"] = self.source
        if self.service is not None:
            payload["service"] = self.service
        if self.trace_id is not None:
            payload["trace_id"] = self.trace_id
        if self.span_id is not None:
            payload["span_id"] = self.span_id
        payload["event_id"] = self.event_id or str(uuid4())
        return payload


@dataclass(frozen=True)
class LogIngestionBatch:
    records: list[LogIngestionRecord]
    source: Optional[str] = None
    service: Optional[str] = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"records": [record.to_payload() for record in self.records]}
        if self.source is not None:
            payload["source"] = self.source
        if self.service is not None:
            payload["service"] = self.service
        return payload


@dataclass(frozen=True)
class LogIngestionResponse:
    accepted: int
    rejected: int = 0
    request_id: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Any) -> "LogIngestionResponse":
        data = _ensure_mapping(payload)
        accepted = data.get("accepted")
        if accepted is None:
            accepted = data.get("ingested") or len(data.get("records") or [])
        rejected = data.get("rejected") or data.get("failed") or 0
        return cls(
            accepted=int(accepted),
            rejected=int(rejected),
            request_id=data.get("request_id") or data.get("id") or data.get("trace_id"),
            raw=data,
        )


def normalize_log_query_request(value: Any) -> dict[str, Any]:
    if isinstance(value, LogQueryRequest):
        return value.to_payload()
    data = _ensure_mapping(value)
    return LogQueryRequest(
        query=str(data.get("query", "")),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
        limit=int(data.get("limit", 1000)),
        cursor=data.get("cursor"),
        filters=_ensure_mapping(data.get("filters")),
    ).to_payload()


def normalize_log_ingestion_record(value: Any) -> dict[str, Any]:
    if isinstance(value, LogIngestionRecord):
        return value.to_payload()
    data = _ensure_mapping(value)
    return LogIngestionRecord(
        message=str(data.get("message", "")),
        timestamp=data.get("timestamp"),
        level=str(data.get("level", "info")),
        source=data.get("source"),
        service=data.get("service"),
        labels=_ensure_mapping(data.get("labels")),
        attributes=_ensure_mapping(data.get("attributes")),
        trace_id=data.get("trace_id"),
        span_id=data.get("span_id"),
        event_id=data.get("event_id"),
    ).to_payload()


def normalize_log_ingestion_batch(value: Any) -> dict[str, Any]:
    if isinstance(value, LogIngestionBatch):
        return value.to_payload()
    data = _ensure_mapping(value)
    records = data.get("records") or []
    return LogIngestionBatch(
        records=[
            record if isinstance(record, LogIngestionRecord) else LogIngestionRecord(
                message=str(_ensure_mapping(record).get("message", "")),
                timestamp=_ensure_mapping(record).get("timestamp"),
                level=str(_ensure_mapping(record).get("level", "info")),
                source=_ensure_mapping(record).get("source"),
                service=_ensure_mapping(record).get("service"),
                labels=_ensure_mapping(_ensure_mapping(record).get("labels")),
                attributes=_ensure_mapping(_ensure_mapping(record).get("attributes")),
                trace_id=_ensure_mapping(record).get("trace_id"),
                span_id=_ensure_mapping(record).get("span_id"),
                event_id=_ensure_mapping(record).get("event_id"),
            )
            for record in records
        ],
        source=data.get("source"),
        service=data.get("service"),
    ).to_payload()
