from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc(value: Optional[datetime]) -> datetime:
    if value is None:
        return _utc_now()
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _isoformat_utc(value: datetime) -> str:
    return _to_utc(value).isoformat().replace("+00:00", "Z")


def _coerce_str_mapping(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})


def _coerce_tags(value: Optional[Sequence[str] | str]) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item for item in (part.strip() for part in value.split(",")) if item]
    return [str(item) for item in value]


@dataclass(frozen=True)
class LogQueryRequest:
    query: str = "*"
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100
    filters: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "LogQueryRequest":
        return LogQueryRequest(
            query=self.query.strip() or "*",
            start_time=_to_utc(self.start_time) if self.start_time else None,
            end_time=_to_utc(self.end_time) if self.end_time else None,
            limit=max(1, int(self.limit)),
            filters=dict(self.filters),
        )

    def to_params(self) -> Dict[str, Any]:
        normalized = self.normalized()
        params: Dict[str, Any] = {"query": normalized.query, "limit": normalized.limit}
        if normalized.start_time is not None:
            params["start_time"] = _isoformat_utc(normalized.start_time)
        if normalized.end_time is not None:
            params["end_time"] = _isoformat_utc(normalized.end_time)
        if normalized.filters:
            params["filters"] = normalized.filters
        return params


@dataclass(frozen=True)
class LogIngestRecord:
    message: str
    timestamp: datetime = field(default_factory=_utc_now)
    service: str = "observability-client"
    severity: str = "INFO"
    fields: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "LogIngestRecord":
        return LogIngestRecord(
            message=str(self.message),
            timestamp=_to_utc(self.timestamp),
            service=str(self.service).strip() or "observability-client",
            severity=str(self.severity).upper().strip() or "INFO",
            fields=dict(self.fields),
        )

    def to_payload(self) -> Dict[str, Any]:
        normalized = self.normalized()
        payload = {
            "message": normalized.message,
            "timestamp": _isoformat_utc(normalized.timestamp),
            "service": normalized.service,
            "severity": normalized.severity,
        }
        payload.update(normalized.fields)
        return payload


@dataclass(frozen=True)
class LogQueryResponse:
    results: List[Dict[str, Any]]
    raw: Any = None

    @classmethod
    def from_api_response(cls, data: Any) -> "LogQueryResponse":
        if isinstance(data, dict):
            results = data.get("results")
            if isinstance(results, list):
                return cls(results=[dict(item) for item in results if isinstance(item, Mapping)], raw=data)
            if isinstance(data.get("data"), list):
                return cls(results=[dict(item) for item in data["data"] if isinstance(item, Mapping)], raw=data)
        if isinstance(data, list):
            return cls(results=[dict(item) for item in data if isinstance(item, Mapping)], raw=data)
        return cls(results=[], raw=data)


@dataclass(frozen=True)
class LogIngestResponse:
    accepted: int
    raw: Any = None

    @classmethod
    def from_api_response(cls, data: Any, fallback_accepted: int = 0) -> "LogIngestResponse":
        if isinstance(data, dict):
            accepted = data.get("accepted")
            if isinstance(accepted, int):
                return cls(accepted=accepted, raw=data)
            ingested = data.get("ingested")
            if isinstance(ingested, int):
                return cls(accepted=ingested, raw=data)
        return cls(accepted=int(fallback_accepted), raw=data)


def normalize_log_record(value: Mapping[str, Any] | LogIngestRecord) -> Dict[str, Any]:
    if isinstance(value, LogIngestRecord):
        return value.to_payload()
    record = dict(value)
    record["message"] = str(record.get("message", ""))
    timestamp = record.get("timestamp")
    if isinstance(timestamp, datetime):
        record["timestamp"] = _isoformat_utc(timestamp)
    elif not timestamp:
        record["timestamp"] = _isoformat_utc(_utc_now())
    service = str(record.get("service", "observability-client")).strip() or "observability-client"
    record["service"] = service
    severity = str(record.get("severity", "INFO")).upper().strip() or "INFO"
    record["severity"] = severity
    return record


def normalize_query_filters(filters: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in _coerce_str_mapping(filters).items():
        if value is None:
            continue
        if isinstance(value, datetime):
            normalized[key] = _isoformat_utc(value)
        elif isinstance(value, (list, tuple, set)):
            normalized[key] = [str(item) for item in value]
        else:
            normalized[key] = value
    return normalized


def build_query_request(
    query: str = "*",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
    filters: Optional[Mapping[str, Any]] = None,
) -> LogQueryRequest:
    return LogQueryRequest(
        query=query,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        filters=normalize_query_filters(filters),
    ).normalized()


def build_ingest_record(
    message: str,
    *,
    service: str = "observability-client",
    severity: str = "INFO",
    timestamp: Optional[datetime] = None,
    **fields: Any,
) -> LogIngestRecord:
    return LogIngestRecord(
        message=message,
        timestamp=timestamp or _utc_now(),
        service=service,
        severity=severity,
        fields=dict(fields),
    ).normalized()
