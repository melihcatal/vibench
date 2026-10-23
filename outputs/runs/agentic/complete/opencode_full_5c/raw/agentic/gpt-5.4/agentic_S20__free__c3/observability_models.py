from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_timestamp(value: Optional[str]) -> str:
    if not value:
        return utc_now_iso()
    if value.endswith("Z"):
        return value
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return utc_now_iso()
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def compact_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


@dataclass
class StructuredLogEvent:
    service: str
    environment: str
    message: str
    level: str = "INFO"
    ddsource: str = "python"
    ddtags: List[str] = field(default_factory=list)
    hostname: Optional[str] = None
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.level.lower(),
            "ddsource": self.ddsource,
            "ddtags": ",".join(self.ddtags),
            "timestamp": normalize_timestamp(self.timestamp),
            "environment": self.environment,
        }
        if self.hostname:
            payload["hostname"] = self.hostname
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.attributes)
        return payload


@dataclass
class LogQueryWindow:
    start: str
    end: str

    def to_datadog_filter(self) -> Dict[str, str]:
        return {
            "from": normalize_timestamp(self.start),
            "to": normalize_timestamp(self.end),
        }


@dataclass
class RetrievedLog:
    id: str
    timestamp: str
    message: str
    service: Optional[str]
    status: Optional[str]
    attributes: Dict[str, Any]


def normalize_datadog_log_item(item: Dict[str, Any]) -> RetrievedLog:
    attributes = item.get("attributes", {})
    return RetrievedLog(
        id=item.get("id", ""),
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        status=attributes.get("status"),
        attributes=attributes,
    )


def extract_log_messages(logs: List[RetrievedLog]) -> List[str]:
    return [log.message for log in logs if log.message]
