from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional
import json


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_rfc3339(value: Optional[str | datetime]) -> str:
    if value is None:
        return utc_now().isoformat()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    return value


def iso_window(minutes: int) -> tuple[str, str]:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    return start.isoformat(), end.isoformat()


@dataclass
class StructuredLogEvent:
    message: str
    severity: str = "INFO"
    service: str = "application"
    correlation_id: Optional[str] = None
    timestamp: Optional[str | datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_entry(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "service": self.service,
            "severity": self.severity,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.extra_fields)
        return {
            "timestamp": ensure_rfc3339(self.timestamp),
            "severity": self.severity,
            "labels": dict(self.labels),
            "jsonPayload": payload,
        }


@dataclass
class LogQueryWindow:
    start_time: str
    end_time: str

    @classmethod
    def last_minutes(cls, minutes: int) -> "LogQueryWindow":
        start, end = iso_window(minutes)
        return cls(start_time=start, end_time=end)


@dataclass
class NormalizedLogRecord:
    timestamp: str
    severity: str
    message: str
    service: Optional[str]
    correlation_id: Optional[str]
    labels: Dict[str, Any]
    raw: Dict[str, Any]


def extract_json_payload(entry: Dict[str, Any]) -> Dict[str, Any]:
    payload = entry.get("jsonPayload") or {}
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"message": payload}
    if isinstance(payload, dict):
        return payload
    return {}


def normalize_log_entry(entry: Dict[str, Any]) -> NormalizedLogRecord:
    payload = extract_json_payload(entry)
    labels = entry.get("labels") or {}
    return NormalizedLogRecord(
        timestamp=entry.get("timestamp", ""),
        severity=entry.get("severity") or payload.get("severity", "DEFAULT"),
        message=payload.get("message") or entry.get("textPayload", ""),
        service=payload.get("service") or labels.get("service"),
        correlation_id=payload.get("correlation_id") or labels.get("correlation_id"),
        labels=labels,
        raw=entry,
    )


def normalize_log_entries(
    entries: Iterable[Dict[str, Any]],
) -> List[NormalizedLogRecord]:
    return [normalize_log_entry(entry) for entry in entries]


def summarize_records(records: Iterable[NormalizedLogRecord]) -> Dict[str, Any]:
    collected = list(records)
    by_severity: Dict[str, int] = {}
    services: Dict[str, int] = {}
    for record in collected:
        by_severity[record.severity] = by_severity.get(record.severity, 0) + 1
        if record.service:
            services[record.service] = services.get(record.service, 0) + 1
    return {
        "count": len(collected),
        "by_severity": by_severity,
        "services": services,
        "records": [record.raw for record in collected],
    }
