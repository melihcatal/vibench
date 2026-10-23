from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_iso8601(value: Optional[str]) -> str:
    if value:
        return value
    return utc_now_iso()


@dataclass
class LogEvent:
    message: str
    service: str
    severity: str = "INFO"
    timestamp: Optional[str] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> Dict[str, Any]:
        record: Dict[str, Any] = {
            "timestamp": ensure_iso8601(self.timestamp),
            "message": self.message,
            "service": self.service,
            "status": self.severity.upper(),
        }
        if self.correlation_id:
            record["correlation_id"] = self.correlation_id
        if self.request_id:
            record["request_id"] = self.request_id
        record.update(self.attributes)
        return record

    def to_json(self) -> str:
        return json.dumps(self.to_record(), separators=(",", ":"), ensure_ascii=False)


@dataclass
class LogQuery:
    start_time: str
    end_time: str
    query: str
    limit: int = 100


@dataclass
class NormalizedLogEntry:
    timestamp: str
    message: str
    severity: str
    service: Optional[str]
    correlation_id: Optional[str]
    raw: Dict[str, Any]


@dataclass
class IncidentSummary:
    summary: str
    affected_services: List[str]
    top_errors: List[str]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogEntry:
    attributes = item.get("attributes", {})
    return NormalizedLogEntry(
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        severity=str(attributes.get("status", "")).upper(),
        service=attributes.get("service"),
        correlation_id=attributes.get("attributes", {}).get("correlation_id")
        or attributes.get("request_id"),
        raw=item,
    )


def serialize_log_entries(entries: List[NormalizedLogEntry]) -> str:
    return json.dumps(
        [
            {
                "timestamp": entry.timestamp,
                "message": entry.message,
                "severity": entry.severity,
                "service": entry.service,
                "correlation_id": entry.correlation_id,
            }
            for entry in entries
        ],
        ensure_ascii=False,
    )
