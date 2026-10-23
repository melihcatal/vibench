from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_correlation_id(value: Optional[str] = None) -> str:
    return value or str(uuid.uuid4())


@dataclass
class StructuredLogEvent:
    message: str
    service: str
    source: str
    tags: List[str] = field(default_factory=list)
    hostname: Optional[str] = None
    status: str = "info"
    timestamp: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_event(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "ddsource": self.source,
            "ddtags": ",".join(self.tags),
            "status": self.status,
            "timestamp": self.timestamp or utc_now_iso(),
        }
        if self.hostname:
            payload["hostname"] = self.hostname
        payload.update(self.attributes)
        return payload


@dataclass
class CorrelatedLogEvent(StructuredLogEvent):
    correlation_id: str = field(default_factory=ensure_correlation_id)

    def to_datadog_event(self) -> Dict[str, Any]:
        payload = super().to_datadog_event()
        payload["correlation_id"] = self.correlation_id
        return payload


@dataclass
class LogQueryRequest:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "desc"

    def to_datadog_payload(self) -> Dict[str, Any]:
        return {
            "filter": {
                "query": self.query,
                "from": self.from_time,
                "to": self.to_time,
            },
            "page": {"limit": self.limit},
            "sort": self.sort,
        }


@dataclass
class NormalizedLogRecord:
    id: str
    timestamp: str
    message: str
    status: str
    service: Optional[str]
    attributes: Dict[str, Any]


@dataclass
class LogQueryResponse:
    records: List[NormalizedLogRecord]
    raw: Dict[str, Any]


def normalize_datadog_logs(items: Iterable[Dict[str, Any]]) -> List[NormalizedLogRecord]:
    normalized: List[NormalizedLogRecord] = []
    for item in items:
        attributes = item.get("attributes", {})
        normalized.append(
            NormalizedLogRecord(
                id=item.get("id", ""),
                timestamp=attributes.get("timestamp", ""),
                message=attributes.get("message", ""),
                status=attributes.get("status", ""),
                service=attributes.get("service"),
                attributes=attributes,
            )
        )
    return normalized
