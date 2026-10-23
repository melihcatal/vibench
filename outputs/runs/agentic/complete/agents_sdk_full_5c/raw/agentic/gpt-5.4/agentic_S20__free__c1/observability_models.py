from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


@dataclass
class StructuredLogEvent:
    message: str
    service: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self) -> Dict[str, Any]:
        ts = self.timestamp or datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.severity.lower(),
            "timestamp": ts.isoformat(),
            "ddsource": "python",
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.attributes)
        return payload


@dataclass
class LogQueryRequest:
    query: str
    from_time: datetime
    to_time: datetime
    limit: int = 50
    sort: str = "desc"

    def to_datadog_payload(self) -> Dict[str, Any]:
        return {
            "filter": {
                "from": self.from_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "to": self.to_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "query": self.query,
            },
            "sort": self.sort,
            "page": {"limit": self.limit},
        }


@dataclass
class NormalizedLogRecord:
    timestamp: Optional[str]
    message: str
    service: Optional[str]
    severity: Optional[str]
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQueryResponse:
    records: List[NormalizedLogRecord]
    raw: Dict[str, Any]


def normalize_datadog_log_item(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp"),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        severity=attributes.get("status"),
        attributes=attributes,
    )


def logs_to_text(records: List[NormalizedLogRecord]) -> str:
    lines: List[str] = []
    for record in records:
        stamp = record.timestamp or "unknown-time"
        sev = record.severity or "unknown-severity"
        svc = record.service or "unknown-service"
        lines.append(f"[{stamp}] {sev} {svc}: {record.message}")
    return "\n".join(lines)


def compact_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str)
