from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_correlation_id(value: Optional[str] = None) -> str:
    return value or str(uuid.uuid4())


@dataclass
class LogEvent:
    message: str
    service: str
    source: str
    host: str
    status: str = "info"
    tags: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None

    def to_datadog_http(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "ddsource": self.source,
            "hostname": self.host,
            "status": self.status,
            "ddtags": ",".join(self.tags),
        }
        payload.update(self.attributes)
        payload["timestamp"] = self.timestamp or utc_now_iso()
        return payload


@dataclass
class CorrelatedLogBatch:
    request_id: str
    events: List[LogEvent]

    def to_datadog_http(self) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        for event in self.events:
            data = event.to_datadog_http()
            data["request_id"] = self.request_id
            normalized.append(data)
        return normalized


@dataclass
class LogQueryRequest:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "timestamp"

    def to_datadog_payload(self, columns: Optional[List[str]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "filter": {
                "query": self.query,
                "from": self.from_time,
                "to": self.to_time,
            },
            "sort": self.sort,
            "page": {"limit": self.limit},
        }
        if columns:
            payload["options"] = {"timeOffset": 0}
            payload["columns"] = columns
        return payload


@dataclass
class NormalizedLogRecord:
    timestamp: Optional[str]
    message: str
    service: Optional[str]
    status: Optional[str]
    attributes: Dict[str, Any]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp"),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        status=attributes.get("status"),
        attributes=attributes,
    )
