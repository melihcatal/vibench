from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def _iso(ts: Optional[datetime] = None) -> str:
    ts = ts or datetime.now(timezone.utc)
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class LogEvent:
    message: str
    service: str
    status: str = "info"
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_payload(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "service": self.service,
            "status": self.status,
            "timestamp": _iso(self.timestamp),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.request_id:
            payload["request_id"] = self.request_id
        payload.update(self.attributes)
        return payload


@dataclass(frozen=True)
class LogQuery:
    query: str
    start_time: datetime
    end_time: datetime
    limit: int = 50

    def to_datadog_payload(self) -> Dict[str, Any]:
        return {
            "filter": {
                "query": self.query,
                "from": _iso(self.start_time),
                "to": _iso(self.end_time),
            },
            "page": {"limit": self.limit},
        }


@dataclass(frozen=True)
class NormalizedLogResult:
    message: str
    status: str
    service: Optional[str] = None
    timestamp: Optional[str] = None
    correlation_id: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_query_response(response: Any) -> Dict[str, Any]:
    if isinstance(response, dict):
        data = response.get("data", response)
    else:
        data = response
    items: List[NormalizedLogResult] = []
    if isinstance(data, dict):
        records = data.get("attributes", {}).get("results") or data.get("results") or data.get("data") or []
    else:
        records = data or []
    for record in records:
        attrs = record.get("attributes", record) if isinstance(record, dict) else {}
        items.append(
            NormalizedLogResult(
                message=str(attrs.get("message", attrs.get("msg", ""))),
                status=str(attrs.get("status", attrs.get("level", ""))),
                service=attrs.get("service"),
                timestamp=attrs.get("timestamp") or attrs.get("date"),
                correlation_id=attrs.get("correlation_id") or attrs.get("request_id"),
                raw=record if isinstance(record, dict) else {"value": record},
            )
        )
    return {"count": len(items), "results": [item.__dict__ for item in items]}
