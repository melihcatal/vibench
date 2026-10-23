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


def compact_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


@dataclass
class LogEvent:
    message: str
    level: str = "INFO"
    service: str = "application"
    source: str = "python"
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "status": self.level.lower(),
            "service": self.service,
            "source": self.source,
            "timestamp": ensure_iso8601(self.timestamp),
        }
        if self.tags:
            payload["ddtags"] = ",".join(self.tags)
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.attributes)
        return payload


@dataclass
class LogQuery:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "desc"


@dataclass
class NormalizedLogRecord:
    timestamp: str
    message: str
    service: str
    status: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQueryResponse:
    records: List[NormalizedLogRecord]
    raw: Dict[str, Any]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        service=attributes.get("service", ""),
        status=attributes.get("status", ""),
        attributes=attributes,
    )


def normalize_datadog_search_response(payload: Dict[str, Any]) -> LogQueryResponse:
    records = [normalize_datadog_log(item) for item in payload.get("data", [])]
    return LogQueryResponse(records=records, raw=payload)
