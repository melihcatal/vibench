from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Sequence


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    raw = value.strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    parsed = datetime.fromisoformat(raw)
    return _ensure_utc(parsed)


def _format_datetime(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return _ensure_utc(value).isoformat().replace("+00:00", "Z")


def _coerce_tags(tags: Optional[Sequence[str]]) -> List[str]:
    if not tags:
        return []
    return [str(tag) for tag in tags if str(tag)]


def _coerce_context(context: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(context or {})


@dataclass(frozen=True)
class ManagedLogQueryRequest:
    query: str
    start_time: datetime
    end_time: datetime
    limit: int = 100
    cursor: Optional[str] = None

    def normalized(self) -> "ManagedLogQueryRequest":
        return ManagedLogQueryRequest(
            query=self.query.strip(),
            start_time=_ensure_utc(self.start_time),
            end_time=_ensure_utc(self.end_time),
            limit=max(1, int(self.limit)),
            cursor=self.cursor.strip() if self.cursor else None,
        )

    def to_payload(self) -> Dict[str, Any]:
        normalized = self.normalized()
        payload: Dict[str, Any] = {
            "query": normalized.query,
            "from": _format_datetime(normalized.start_time),
            "to": _format_datetime(normalized.end_time),
            "limit": normalized.limit,
        }
        if normalized.cursor:
            payload["cursor"] = normalized.cursor
        return payload


@dataclass(frozen=True)
class ManagedLogQueryResponse:
    records: List[Dict[str, Any]] = field(default_factory=list)
    next_cursor: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedLogQueryResponse":
        data = dict(payload or {})
        records = data.get("data") or data.get("records") or []
        next_cursor = data.get("next_cursor") or data.get("nextCursor") or data.get("cursor")
        if not isinstance(records, list):
            records = [records]
        return cls(records=[dict(item) if isinstance(item, Mapping) else {"value": item} for item in records], next_cursor=next_cursor, raw=data)


@dataclass(frozen=True)
class ManagedLogIngestionRequest:
    event_name: str
    severity: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "ManagedLogIngestionRequest":
        return ManagedLogIngestionRequest(
            event_name=self.event_name.strip(),
            severity=self.severity.strip().upper(),
            payload=dict(self.payload),
            timestamp=_ensure_utc(self.timestamp),
            source=self.source.strip() if self.source else None,
            tags=_coerce_tags(self.tags),
            context=_coerce_context(self.context),
        )

    def to_record(self) -> Dict[str, Any]:
        normalized = self.normalized()
        record = {
            "timestamp": _format_datetime(normalized.timestamp),
            "event_name": normalized.event_name,
            "severity": normalized.severity,
            "payload": normalized.payload,
        }
        if normalized.source:
            record["source"] = normalized.source
        if normalized.tags:
            record["tags"] = normalized.tags
        if normalized.context:
            record["context"] = normalized.context
        return record


@dataclass(frozen=True)
class ManagedLogIngestionResponse:
    accepted: bool
    record_count: int
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedLogIngestionResponse":
        data = dict(payload or {})
        accepted = bool(data.get("accepted", True))
        record_count = data.get("record_count", data.get("count", 0))
        return cls(accepted=accepted, record_count=int(record_count), raw=data)


def normalize_managed_log_query_request(request: ManagedLogQueryRequest) -> Dict[str, Any]:
    return request.normalized().to_payload()


def normalize_managed_log_ingestion_request(request: ManagedLogIngestionRequest) -> Dict[str, Any]:
    return request.normalized().to_record()


def parse_managed_log_query_response(payload: Mapping[str, Any]) -> ManagedLogQueryResponse:
    return ManagedLogQueryResponse.from_payload(payload)


def parse_managed_log_ingestion_response(payload: Mapping[str, Any]) -> ManagedLogIngestionResponse:
    return ManagedLogIngestionResponse.from_payload(payload)


def parse_iso8601(value: Optional[str]) -> Optional[datetime]:
    return _parse_datetime(value)
