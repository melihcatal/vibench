from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_iso8601(value: str | None) -> str:
    if value:
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized).astimezone(timezone.utc).isoformat()
    return utc_now_iso()


def compact_json(value: dict[str, Any]) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


@dataclass(slots=True)
class LogEvent:
    message: str
    service: str
    level: str = "INFO"
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_datadog(
        self, ddsource: str = "python", ddtags: str | None = None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.level.lower(),
            "timestamp": ensure_iso8601(self.timestamp),
            "ddsource": ddsource,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if ddtags:
            payload["ddtags"] = ddtags
        payload.update(self.attributes)
        return payload


@dataclass(slots=True)
class LogQuery:
    query: str
    from_time: str
    to_time: str
    limit: int = 50
    sort: str = "desc"

    def to_datadog_filter(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "from": ensure_iso8601(self.from_time),
            "to": ensure_iso8601(self.to_time),
        }

    def to_datadog_page(self) -> dict[str, Any]:
        return {"limit": self.limit}

    def to_datadog_sort(self) -> str:
        return "timestamp" if self.sort == "asc" else "-timestamp"


@dataclass(slots=True)
class NormalizedLogRecord:
    timestamp: str
    message: str
    service: str | None
    status: str | None
    correlation_id: str | None
    attributes: dict[str, Any]


@dataclass(slots=True)
class QueryResult:
    records: list[NormalizedLogRecord]
    total: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "records": [asdict(record) for record in self.records],
        }


def normalize_datadog_log(item: Any) -> NormalizedLogRecord:
    attributes = dict(getattr(item, "attributes", {}) or {})
    return NormalizedLogRecord(
        timestamp=str(attributes.get("timestamp") or ""),
        message=str(attributes.get("message") or ""),
        service=attributes.get("service"),
        status=attributes.get("status"),
        correlation_id=attributes.get("correlation_id"),
        attributes=attributes,
    )
