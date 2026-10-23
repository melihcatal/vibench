from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class LogEvent:
    service: str
    level: str
    message: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: Optional[str] = None
    environment: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "service": self.service,
            "level": self.level.upper(),
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.environment:
            payload["environment"] = self.environment
        payload.update(self.fields)
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_payload(), separators=(",", ":"), ensure_ascii=False)


@dataclass
class LogQueryRequest:
    query: str
    from_time: str
    to_time: str
    limit: int = 50


@dataclass
class NormalizedLogRecord:
    timestamp: str
    message: str
    level: str
    service: Optional[str]
    correlation_id: Optional[str]
    raw: Dict[str, Any]


@dataclass
class LogQueryResponse:
    records: List[NormalizedLogRecord]


@dataclass
class IncidentSummary:
    summary: str
    total_errors: int
    affected_services: List[str]


def ensure_correlation_id(correlation_id: Optional[str] = None) -> str:
    return correlation_id or str(uuid.uuid4())


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attrs = item.get("attributes", {})
    attrs_nested = attrs.get("attributes", {}) if isinstance(attrs.get("attributes"), dict) else {}
    message = attrs.get("message") or attrs_nested.get("message") or ""
    level = attrs.get("status") or attrs_nested.get("level") or attrs_nested.get("status") or "INFO"
    service = attrs.get("service") or attrs_nested.get("service")
    correlation_id = (
        attrs_nested.get("correlation_id")
        or attrs_nested.get("request_id")
        or attrs.get("correlation_id")
    )
    timestamp = attrs.get("timestamp") or item.get("id", "")
    return NormalizedLogRecord(
        timestamp=timestamp,
        message=message,
        level=str(level).upper(),
        service=service,
        correlation_id=correlation_id,
        raw=item,
    )
