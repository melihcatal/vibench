from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_iso8601(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def now_iso8601() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_log_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    if "timestamp" in data and isinstance(data["timestamp"], str):
        data["timestamp"] = normalize_iso8601(data["timestamp"])
    else:
        data["timestamp"] = now_iso8601()
    if "severity" in data and isinstance(data["severity"], str):
        data["severity"] = data["severity"].upper()
    return data


@dataclass
class LogIngestionRequest:
    event: Dict[str, Any]

    def to_payload(self) -> Dict[str, Any]:
        return normalize_log_event(self.event)


@dataclass
class LogQueryRequest:
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = 100

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"limit": self.limit}
        if self.severity:
            payload["severity"] = self.severity.upper()
        if self.field_filters:
            payload["field_filters"] = self.field_filters
        if self.start_time:
            payload["start_time"] = normalize_iso8601(self.start_time)
        if self.end_time:
            payload["end_time"] = normalize_iso8601(self.end_time)
        return payload


@dataclass
class LogResponse:
    items: List[Dict[str, Any]]
