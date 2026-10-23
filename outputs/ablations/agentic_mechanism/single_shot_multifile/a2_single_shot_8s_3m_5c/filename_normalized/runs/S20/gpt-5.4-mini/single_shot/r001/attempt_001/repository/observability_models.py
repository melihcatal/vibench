from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


SEVERITY_ALIASES = {
    "debug": "DEBUG",
    "info": "INFO",
    "warning": "WARNING",
    "warn": "WARNING",
    "error": "ERROR",
    "critical": "CRITICAL",
    "alert": "ALERT",
    "emergency": "EMERGENCY",
}


@dataclass(frozen=True)
class LogWindow:
    start_time: datetime
    end_time: datetime

    def to_rfc3339(self) -> Dict[str, str]:
        return {"start_time": to_rfc3339(self.start_time), "end_time": to_rfc3339(self.end_time)}


@dataclass(frozen=True)
class LogQueryRequest:
    severity: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    window: Optional[LogWindow] = None
    limit: int = 100


@dataclass(frozen=True)
class LogWriteRequest:
    payload: Dict[str, Any]
    severity: str = "INFO"
    log_name: Optional[str] = None


@dataclass(frozen=True)
class LogSummary:
    total: int
    by_severity: Dict[str, int]
    messages: List[str]


def to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_severity(severity: str) -> str:
    return SEVERITY_ALIASES.get(severity.lower(), severity.upper())


def normalize_log_fields(payload: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, datetime):
            normalized[key] = to_rfc3339(value)
        elif isinstance(value, Mapping):
            normalized[key] = normalize_log_fields(value)
        elif isinstance(value, list):
            normalized[key] = [normalize_log_fields(v) if isinstance(v, Mapping) else v for v in value]
        else:
            normalized[key] = value
    return normalized


def build_filter(query: LogQueryRequest) -> str:
    parts: List[str] = []
    if query.severity:
        parts.append(f'severity>={normalize_severity(query.severity)}')
    if query.field_name and query.field_value is not None:
        parts.append(f'{query.field_name}="{query.field_value}"')
    if query.window:
        parts.append(f'timestamp>="{to_rfc3339(query.window.start_time)}"')
        parts.append(f'timestamp<="{to_rfc3339(query.window.end_time)}"')
    return " AND ".join(parts)


def summarize_entries(entries: Iterable[Mapping[str, Any]]) -> LogSummary:
    total = 0
    by_severity: Dict[str, int] = {}
    messages: List[str] = []
    for entry in entries:
        total += 1
        severity = str(entry.get("severity", "UNKNOWN"))
        by_severity[severity] = by_severity.get(severity, 0) + 1
        msg = entry.get("textPayload") or entry.get("jsonPayload", {}).get("message") or ""
        if msg:
            messages.append(str(msg))
    return LogSummary(total=total, by_severity=by_severity, messages=messages)
