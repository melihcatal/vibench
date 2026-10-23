from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json


@dataclass(slots=True)
class StructuredLogEvent:
    service: str
    environment: str
    message: str
    severity: str = "INFO"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str | None = None
    trace_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_cloud_logging_entry(self) -> dict[str, Any]:
        payload = {
            "service": self.service,
            "environment": self.environment,
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.request_id:
            payload["request_id"] = self.request_id
        if self.trace_id:
            payload["trace_id"] = self.trace_id
        payload.update(self.attributes)
        return payload


@dataclass(slots=True)
class LogQuery:
    resource_names: list[str]
    filter_text: str
    page_size: int = 50


@dataclass(slots=True)
class LogRecord:
    timestamp: str
    severity: str
    message: str
    payload: dict[str, Any]


def ensure_rfc3339(value: datetime | str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def normalize_logging_entry(entry: dict[str, Any]) -> LogRecord:
    payload = entry.get("jsonPayload") or {}
    text_payload = entry.get("textPayload")
    if text_payload and not payload:
        payload = {"message": text_payload}
    message = str(payload.get("message") or entry.get("textPayload") or "")
    return LogRecord(
        timestamp=entry.get("timestamp", ""),
        severity=entry.get("severity", "DEFAULT"),
        message=message,
        payload=payload,
    )


def as_pretty_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, default=str)
