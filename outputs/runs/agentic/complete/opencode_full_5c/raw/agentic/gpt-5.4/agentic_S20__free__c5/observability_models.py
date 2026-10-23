from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_correlation_id(value: str | None = None) -> str:
    return value or str(uuid.uuid4())


def normalize_severity(value: str) -> str:
    return value.upper().strip()


def compact_json(value: dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


@dataclass(slots=True)
class LogEvent:
    service: str
    level: str
    message: str
    correlation_id: str | None = None
    timestamp: str = field(default_factory=utc_now_iso)
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_datadog_tags(self) -> str:
        parts = [
            f"service:{self.service}",
            f"level:{normalize_severity(self.level).lower()}",
        ]
        if self.correlation_id:
            parts.append(f"correlation_id:{self.correlation_id}")
        for key, value in sorted(self.attributes.items()):
            if isinstance(value, (str, int, float, bool)):
                parts.append(f"{key}:{value}")
        return ",".join(parts)

    def to_datadog_payload(self, hostname: str) -> dict[str, Any]:
        payload = {
            "message": self.message,
            "service": self.service,
            "hostname": hostname,
            "status": normalize_severity(self.level).lower(),
            "timestamp": self.timestamp,
            "ddsource": "python",
            "attributes": dict(self.attributes),
        }
        if self.correlation_id:
            payload["attributes"]["correlation_id"] = self.correlation_id
        return payload


@dataclass(slots=True)
class LogQueryRequest:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "timestamp"


@dataclass(slots=True)
class LogRecord:
    id: str
    timestamp: str
    message: str
    service: str | None
    status: str | None
    attributes: dict[str, Any]


@dataclass(slots=True)
class LogQueryResponse:
    records: list[LogRecord]
    total: int


def parse_datadog_log_item(item: dict[str, Any]) -> LogRecord:
    attributes = item.get("attributes", {})
    return LogRecord(
        id=item.get("id", ""),
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        status=attributes.get("status"),
        attributes=attributes,
    )


def parse_datadog_search_response(payload: dict[str, Any]) -> LogQueryResponse:
    data = payload.get("data", [])
    records = [parse_datadog_log_item(item) for item in data]
    meta = payload.get("meta", {})
    page = meta.get("page", {})
    total = page.get("total_count", len(records))
    return LogQueryResponse(records=records, total=total)
