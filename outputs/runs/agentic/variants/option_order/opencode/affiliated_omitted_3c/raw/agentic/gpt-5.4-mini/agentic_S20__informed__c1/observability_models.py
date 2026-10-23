from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_timestamp(value: Optional[str] = None) -> str:
    return value or utc_now_iso()


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(fields or {})


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    timestamp: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": normalize_timestamp(self.timestamp),
            "fields": normalize_fields(self.fields),
        }


@dataclass
class LogQuery:
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = 50

    def to_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": self.limit}
        if self.severity:
            params["severity"] = self.severity
        if self.field_filters:
            params.update({f"field_{k}": v for k, v in self.field_filters.items()})
        if self.start_time:
            params["start_time"] = self.start_time
        if self.end_time:
            params["end_time"] = self.end_time
        return params
