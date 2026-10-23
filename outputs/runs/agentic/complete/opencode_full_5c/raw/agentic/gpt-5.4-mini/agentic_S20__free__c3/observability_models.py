from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_timestamp(value: Optional[str] = None) -> str:
    if value:
        return value
    return datetime.now(timezone.utc).isoformat()


def normalize_severity(value: Optional[str]) -> str:
    return (value or "INFO").upper()


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    service: str = "app"
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": normalize_severity(self.severity),
            "service": self.service,
            "timestamp": normalize_timestamp(self.timestamp),
        }
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.correlation_id is not None:
            payload["correlation_id"] = self.correlation_id
        if self.fields:
            payload.update(self.fields)
        return payload


@dataclass
class LogQuery:
    start_time: str
    end_time: str
    severity: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    limit: int = 50

    def to_filter(self) -> Dict[str, Any]:
        filt: Dict[str, Any] = {
            "startTime": self.start_time,
            "endTime": self.end_time,
            "limit": self.limit,
        }
        if self.severity:
            filt["severity"] = normalize_severity(self.severity)
        if self.field_name and self.field_value is not None:
            filt["fieldName"] = self.field_name
            filt["fieldValue"] = self.field_value
        return filt


def extract_messages(items: List[Dict[str, Any]]) -> List[str]:
    return [str(item.get("message", "")) for item in items]
