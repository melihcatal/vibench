from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Union


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _coerce_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        return int(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "items"):
        return dict(value.items())
    return {"value": value}


def _coerce_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return list(value)
    return [value]


def _normalize_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(k): normalize_value(v) for k, v in value.items()}
    if hasattr(value, "__dict__"):
        return normalize_value(vars(value))
    return {"value": normalize_value(value)}


def normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        dt = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, Mapping):
        return {str(k): normalize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [normalize_value(v) for v in value]
    if hasattr(value, "to_dict"):
        return normalize_value(value.to_dict())
    if hasattr(value, "__dict__"):
        return normalize_value(vars(value))
    return str(value)


@dataclass
class LogQueryRequest:
    query: str = ""
    filters: Dict[str, Any] = field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100
    cursor: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LogQueryRequest":
        return cls(
            query=_coerce_str(data.get("query")),
            filters=_coerce_dict(data.get("filters")),
            start_time=_coerce_datetime(data.get("start_time") or data.get("startTime")),
            end_time=_coerce_datetime(data.get("end_time") or data.get("endTime")),
            limit=_coerce_int(data.get("limit"), 100),
            cursor=data.get("cursor"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return normalize_value(
            {
                "query": self.query,
                "filters": self.filters,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "limit": self.limit,
                "cursor": self.cursor,
            }
        )


@dataclass
class LogIngestionRecord:
    message: str
    level: str = "INFO"
    timestamp: Optional[datetime] = None
    fields: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LogIngestionRecord":
        return cls(
            message=_coerce_str(data.get("message")),
            level=_coerce_str(data.get("level") or data.get("severity") or "INFO"),
            timestamp=_coerce_datetime(data.get("timestamp") or data.get("time")),
            fields=_coerce_dict(data.get("fields") or data.get("metadata")),
            correlation_id=data.get("correlation_id") or data.get("correlationId"),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "level": self.level,
            "timestamp": self.timestamp,
            "fields": self.fields,
            "correlation_id": self.correlation_id,
        }
        return normalize_value({k: v for k, v in payload.items() if v is not None})


@dataclass
class LogQueryResult:
    entries: List[Dict[str, Any]] = field(default_factory=list)
    next_cursor: Optional[str] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LogQueryResult":
        entries = _coerce_list(data.get("entries") or data.get("results") or data.get("items"))
        return cls(
            entries=[_normalize_mapping(item) for item in entries],
            next_cursor=data.get("next_cursor") or data.get("nextCursor"),
            total=data.get("total"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return normalize_value(
            {
                "entries": self.entries,
                "next_cursor": self.next_cursor,
                "total": self.total,
            }
        )


@dataclass
class IngestionResponse:
    accepted: int = 0
    rejected: int = 0
    request_id: Optional[str] = None
    errors: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "IngestionResponse":
        return cls(
            accepted=_coerce_int(data.get("accepted"), 0),
            rejected=_coerce_int(data.get("rejected"), 0),
            request_id=data.get("request_id") or data.get("requestId"),
            errors=[_normalize_mapping(item) for item in _coerce_list(data.get("errors"))],
        )

    def to_dict(self) -> Dict[str, Any]:
        return normalize_value(
            {
                "accepted": self.accepted,
                "rejected": self.rejected,
                "request_id": self.request_id,
                "errors": self.errors,
            }
        )


def normalize_log_entry(entry: Any) -> Dict[str, Any]:
    return _normalize_mapping(entry)


def normalize_log_entries(entries: Iterable[Any]) -> List[Dict[str, Any]]:
    return [normalize_log_entry(entry) for entry in entries]


def normalize_query_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, LogQueryRequest):
        return payload.to_dict()
    return _normalize_mapping(payload)


def normalize_ingestion_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, LogIngestionRecord):
        return payload.to_dict()
    return _normalize_mapping(payload)
