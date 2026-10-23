from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_jsonable(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): ensure_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [ensure_jsonable(v) for v in value]
    return str(value)


def compact_json(value: Any) -> str:
    return json.dumps(ensure_jsonable(value), separators=(",", ":"), sort_keys=True)


@dataclass
class LogEvent:
    message: str
    service: str
    severity: str = "INFO"
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog(self, source: str = "python") -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.severity.lower(),
            "source": source,
            "timestamp": self.timestamp,
            "attributes": ensure_jsonable(self.attributes),
        }
        if self.correlation_id:
            payload["ddtags"] = f"correlation_id:{self.correlation_id}"
            payload["correlation_id"] = self.correlation_id
        return payload


@dataclass
class LogQueryRequest:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "desc"

    def to_datadog(self) -> Dict[str, Any]:
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
    severity: str
    service: Optional[str]
    attributes: Dict[str, Any]


@dataclass
class NormalizedLogQueryResponse:
    records: List[NormalizedLogRecord]
    raw: Dict[str, Any]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {}) or {}
    return NormalizedLogRecord(
        id=item.get("id", ""),
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        severity=str(attributes.get("status", "")),
        service=attributes.get("service"),
        attributes=ensure_jsonable(attributes),
    )


def normalize_datadog_logs_response(
    payload: Dict[str, Any],
) -> NormalizedLogQueryResponse:
    data = payload.get("data", []) or []
    return NormalizedLogQueryResponse(
        records=[normalize_datadog_log(item) for item in data],
        raw=payload,
    )
