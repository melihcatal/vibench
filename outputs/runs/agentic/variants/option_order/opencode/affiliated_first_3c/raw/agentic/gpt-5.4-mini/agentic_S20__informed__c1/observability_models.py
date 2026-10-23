from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_fields(fields: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(fields or {})


def normalize_severity(severity: Optional[str]) -> str:
    return (severity or "INFO").upper()


def normalize_message(message: Any) -> str:
    return str(message)


@dataclass
class LogEvent:
    timestamp: str
    severity: str
    message: str
    fields: Dict[str, Any]

    @classmethod
    def create(
        cls,
        message: Any,
        severity: str = "INFO",
        fields: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> "LogEvent":
        return cls(
            timestamp=timestamp or utc_now_iso(),
            severity=normalize_severity(severity),
            message=normalize_message(message),
            fields=normalize_fields(fields),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
        }
        payload.update(self.fields)
        return payload


@dataclass
class QueryWindow:
    start_time: str
    end_time: str

    @classmethod
    def recent_minutes(cls, minutes: int) -> "QueryWindow":
        end = datetime.now(timezone.utc)
        start = end - __import__("datetime").timedelta(minutes=minutes)
        return cls(
            start_time=start.isoformat().replace("+00:00", "Z"),
            end_time=end.isoformat().replace("+00:00", "Z"),
        )


def coerce_log_records(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(item) for item in items]
