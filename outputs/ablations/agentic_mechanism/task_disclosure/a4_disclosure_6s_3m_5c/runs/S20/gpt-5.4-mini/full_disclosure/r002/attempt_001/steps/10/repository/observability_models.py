from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence


def _ensure_utc_iso8601(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    text = str(value).strip()
    if not text:
        return datetime.now(timezone.utc).isoformat()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    except ValueError:
        return text


def _coerce_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _coerce_mapping(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(frozen=True)
class LogTimeRange:
    start: str
    end: str

    @classmethod
    def from_values(cls, start: Any, end: Any) -> "LogTimeRange":
        return cls(start=_ensure_utc_iso8601(start), end=_ensure_utc_iso8601(end))

    def to_dict(self) -> Dict[str, str]:
        return {"start": self.start, "end": self.end}


@dataclass(frozen=True)
class LogFilter:
    field: str
    operator: str
    value: Any

    def to_dict(self) -> Dict[str, Any]:
        return {"field": self.field, "operator": self.operator, "value": self.value}


@dataclass(frozen=True)
class LogQueryRequest:
    workspace_id: str
    time_range: LogTimeRange
    filters: Sequence[LogFilter] = field(default_factory=tuple)
    limit: int = 100
    sort_field: str = "timestamp"
    sort_direction: str = "desc"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workspaceId": self.workspace_id,
            "limit": self.limit,
            "timeRange": self.time_range.to_dict(),
            "filters": [flt.to_dict() for flt in self.filters],
            "sort": {"field": self.sort_field, "direction": self.sort_direction},
        }


@dataclass(frozen=True)
class LogIngestionRequest:
    events: Sequence[Mapping[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {"events": [dict(event) for event in self.events]}


@dataclass(frozen=True)
class NormalizedLogRecord:
    timestamp: str
    message: str
    severity: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LogQueryResponse:
    results: List[NormalizedLogRecord]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LogIngestionResponse:
    accepted: int
    rejected: int = 0
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_log_record(record: Mapping[str, Any]) -> NormalizedLogRecord:
    data = _coerce_mapping(record)
    attrs = data.get("attributes")
    if not isinstance(attrs, Mapping):
        attrs = {k: v for k, v in data.items() if k not in {"timestamp", "message", "severity", "attributes"}}
    return NormalizedLogRecord(
        timestamp=_ensure_utc_iso8601(data.get("timestamp") or data.get("time") or data.get("created_at")),
        message=_coerce_str(data.get("message") or data.get("msg") or data.get("log")),
        severity=_coerce_str(data.get("severity") or data.get("level") or "info", "info"),
        attributes=dict(attrs),
        raw=data,
    )


def normalize_query_response(payload: Any) -> LogQueryResponse:
    data = _coerce_mapping(payload)
    results = data.get("results")
    if not isinstance(results, Sequence) or isinstance(results, (str, bytes)):
        results = data.get("logs") if isinstance(data.get("logs"), Sequence) else []
    normalized = [normalize_log_record(item) for item in results if isinstance(item, Mapping)]
    return LogQueryResponse(results=normalized, raw=data)


def normalize_ingestion_response(payload: Any, default_accepted: int = 0) -> LogIngestionResponse:
    data = _coerce_mapping(payload)
    accepted = data.get("accepted")
    rejected = data.get("rejected")
    if accepted is None:
        accepted = data.get("ingested")
    return LogIngestionResponse(
        accepted=_coerce_int(accepted, default_accepted),
        rejected=_coerce_int(rejected, 0),
        raw=data,
    )


def build_log_query_request(
    workspace_id: str,
    start: Any,
    end: Any,
    filters: Optional[Sequence[Mapping[str, Any]]] = None,
    limit: int = 100,
    sort_field: str = "timestamp",
    sort_direction: str = "desc",
) -> LogQueryRequest:
    normalized_filters = []
    for item in filters or []:
        if isinstance(item, Mapping):
            normalized_filters.append(
                LogFilter(
                    field=_coerce_str(item.get("field")),
                    operator=_coerce_str(item.get("operator"), "eq"),
                    value=item.get("value"),
                )
            )
    return LogQueryRequest(
        workspace_id=_coerce_str(workspace_id),
        time_range=LogTimeRange.from_values(start, end),
        filters=tuple(normalized_filters),
        limit=_coerce_int(limit, 100),
        sort_field=_coerce_str(sort_field, "timestamp"),
        sort_direction=_coerce_str(sort_direction, "desc"),
    )
