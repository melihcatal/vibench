from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union


def _utc_timestamp(value: Optional[datetime] = None) -> str:
    value = value or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_filter_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, datetime):
        return f'"{_utc_timestamp(value)}"'
    return f'"{value}"'


def build_time_filter(start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> str:
    clauses: List[str] = []
    if start_time is not None:
        clauses.append(f'timestamp >= "{_utc_timestamp(start_time)}"')
    if end_time is not None:
        clauses.append(f'timestamp <= "{_utc_timestamp(end_time)}"')
    return " AND ".join(clauses)


def build_field_filter(field_filters: Optional[Mapping[str, Any]] = None) -> str:
    clauses: List[str] = []
    for key, value in (field_filters or {}).items():
        clauses.append(f"jsonPayload.{key} = {_coerce_filter_value(value)}")
    return " AND ".join(clauses)


def build_log_filter(
    *,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    severity: Optional[str] = None,
    field_filters: Optional[Mapping[str, Any]] = None,
) -> str:
    clauses: List[str] = []
    time_filter = build_time_filter(start_time=start_time, end_time=end_time)
    field_filter = build_field_filter(field_filters=field_filters)
    if severity:
        clauses.append(f"severity >= {severity}")
    if time_filter:
        clauses.append(time_filter)
    if field_filter:
        clauses.append(field_filter)
    return " AND ".join(clauses)


@dataclass(frozen=True)
class ManagedLogQueryRequest:
    project_id: str
    api_key: str
    hours: int = 24
    limit: int = 100
    severity: Optional[str] = None
    field_filters: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time.replace()
        start_time = end_time.fromtimestamp(end_time.timestamp() - self.hours * 3600, tz=timezone.utc)
        payload = {
            "filter": build_log_filter(
                start_time=start_time,
                end_time=end_time,
                severity=self.severity,
                field_filters=self.field_filters,
            ),
            "orderBy": "timestamp desc",
            "pageSize": self.limit,
        }
        return payload


@dataclass(frozen=True)
class ManagedLogIngestionRequest:
    project_id: str
    api_key: str
    message: str
    severity: str = "INFO"
    service_name: str = "google_cloud_logging"
    fields: Mapping[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return {
            "entries": [
                {
                    "jsonPayload": {
                        "service": self.service_name,
                        "message": self.message,
                        "severity": self.severity,
                        "timestamp": _utc_timestamp(),
                        **dict(self.fields),
                    }
                }
            ]
        }


@dataclass(frozen=True)
class ManagedLogQueryResponse:
    entries: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, response: Mapping[str, Any]) -> "ManagedLogQueryResponse":
        return cls(entries=list(response.get("entries", [])), raw=dict(response))


@dataclass(frozen=True)
class ManagedLogIngestionResponse:
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, response: Mapping[str, Any]) -> "ManagedLogIngestionResponse":
        return cls(raw=dict(response))


def normalize_log_entry(entry: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(entry)
    payload = normalized.get("jsonPayload")
    if isinstance(payload, Mapping):
        normalized["payload"] = dict(payload)
        normalized.setdefault("message", payload.get("message"))
        normalized.setdefault("severity", payload.get("severity"))
        normalized.setdefault("service", payload.get("service"))
    elif "textPayload" in normalized:
        normalized["payload"] = normalized.get("textPayload")
    return normalized


def normalize_log_entries(entries: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_log_entry(entry) for entry in entries]
