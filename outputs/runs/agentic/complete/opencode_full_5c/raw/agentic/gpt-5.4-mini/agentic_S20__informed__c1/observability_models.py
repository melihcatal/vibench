from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def iso_utc(value: Optional[datetime] = None) -> str:
    value = value or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_severity(severity: str) -> str:
    return severity.strip().upper()


def normalize_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in fields.items():
        if value is None:
            continue
        normalized[str(key)] = value
    return normalized


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    service: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": normalize_severity(self.severity),
            "timestamp": iso_utc(self.timestamp),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.service:
            payload["service"] = self.service
        if self.fields:
            payload.update(normalize_fields(self.fields))
        return payload


@dataclass
class QueryWindow:
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def to_filter_args(self) -> Dict[str, str]:
        args: Dict[str, str] = {}
        if self.start_time:
            args["start_time"] = iso_utc(self.start_time)
        if self.end_time:
            args["end_time"] = iso_utc(self.end_time)
        return args


@dataclass
class QueryResult:
    entries: List[Dict[str, Any]]
    next_page_token: Optional[str] = None


def coerce_entries(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_fields(item) for item in items]
