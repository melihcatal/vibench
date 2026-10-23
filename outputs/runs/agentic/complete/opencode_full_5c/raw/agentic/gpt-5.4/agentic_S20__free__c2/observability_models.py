from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_iso8601(value: Optional[str]) -> str:
    if value:
        return value
    return utc_now_iso()


def compact_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


@dataclass
class LogEvent:
    service: str
    level: str
    message: str
    environment: str
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.level.lower(),
            "hostname": self.attributes.get("hostname", self.service),
            "ddsource": self.attributes.get("source", "python"),
            "timestamp": ensure_iso8601(self.timestamp),
            "env": self.environment,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        for key, value in self.attributes.items():
            if key not in payload:
                payload[key] = value
        return payload


@dataclass
class LogQueryRequest:
    query: str
    start_time: str
    end_time: str
    limit: int = 50
    sort: str = "desc"

    def to_datadog_body(self) -> Dict[str, Any]:
        return {
            "filter": {
                "query": self.query,
                "from": ensure_iso8601(self.start_time),
                "to": ensure_iso8601(self.end_time),
            },
            "page": {"limit": self.limit},
            "sort": self.sort,
        }


@dataclass
class NormalizedLogRecord:
    timestamp: Optional[str]
    service: Optional[str]
    severity: Optional[str]
    message: Optional[str]
    correlation_id: Optional[str]
    attributes: Dict[str, Any]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    attr = attributes.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp"),
        service=attributes.get("service"),
        severity=attributes.get("status"),
        message=attributes.get("message"),
        correlation_id=attr.get("correlation_id") or attributes.get("correlation_id"),
        attributes=attr if isinstance(attr, dict) else {},
    )


def new_correlation_id(prefix: str = "req") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def join_field_filters(filters: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key, value in filters.items():
        if value is None:
            continue
        text = str(value).replace('"', '\\"')
        parts.append(f'@{key}:"{text}"')
    return " ".join(parts)
