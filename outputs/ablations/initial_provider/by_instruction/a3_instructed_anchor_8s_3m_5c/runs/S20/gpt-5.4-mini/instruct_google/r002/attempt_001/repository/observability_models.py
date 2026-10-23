from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def isoformat_utc(value: Optional[datetime] = None) -> str:
    value = value or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_labels(labels: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (labels or {}).items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {str(key): value for key, value in (fields or {}).items() if value is not None}


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    labels: Optional[Dict[str, Any]] = None
    fields: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity,
            "labels": normalize_labels(self.labels),
            "fields": normalize_fields(self.fields),
            "timestamp": self.timestamp or isoformat_utc(),
        }
        return payload


@dataclass
class LogQuery:
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = 50

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "field_filters": normalize_fields(self.field_filters),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "limit": self.limit,
        }


def records_from_response(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(item) for item in items]
