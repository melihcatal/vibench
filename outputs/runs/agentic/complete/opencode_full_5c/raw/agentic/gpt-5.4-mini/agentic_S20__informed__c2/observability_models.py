from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def isoformat_utc(value: Optional[datetime] = None) -> str:
    dt = value or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(fields or {})


@dataclass
class LogEvent:
    timestamp: str
    service: str
    severity: str
    message: str
    fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        service: str,
        severity: str,
        message: str,
        fields: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> "LogEvent":
        return cls(
            timestamp=isoformat_utc(timestamp),
            service=service,
            severity=severity,
            message=message,
            fields=normalize_fields(fields),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "timestamp": self.timestamp,
            "service": self.service,
            "severity": self.severity,
            "message": self.message,
        }
        payload.update(self.fields)
        return payload


@dataclass
class QueryRequest:
    start_time: str
    end_time: str
    severity: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 100

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "limit": self.limit,
        }
        if self.severity:
            payload["severity"] = self.severity
        payload["field_filters"] = normalize_fields(self.field_filters)
        return payload


@dataclass
class QueryResult:
    items: List[Dict[str, Any]]
    next_token: Optional[str] = None
