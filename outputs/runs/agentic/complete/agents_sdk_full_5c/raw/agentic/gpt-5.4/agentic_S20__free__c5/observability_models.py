from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json


@dataclass
class StructuredLogEvent:
    message: str
    severity: str = "INFO"
    service: str = "application"
    environment: str = "production"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self, ddsource: str = "python", ddtags: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "status": self.severity.lower(),
            "service": self.service,
            "host": self.attributes.get("host", self.service),
            "ddsource": ddsource,
            "timestamp": self.timestamp.isoformat(),
            "environment": self.environment,
            "attributes": self.attributes,
        }
        if ddtags:
            payload["ddtags"] = ",".join(ddtags)
        if self.correlation_id:
            payload["attributes"]["correlation_id"] = self.correlation_id
        return payload


@dataclass
class LogQueryRequest:
    query: str
    from_time: datetime
    to_time: datetime
    limit: int = 25
    sort: str = "desc"

    def to_datadog_filter(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "from": self.from_time.isoformat(),
            "to": self.to_time.isoformat(),
            "indexes": ["*"],
        }

    def to_datadog_page(self) -> Dict[str, Any]:
        return {"limit": self.limit}

    def to_datadog_sort(self) -> str:
        return self.sort


@dataclass
class NormalizedLogRecord:
    timestamp: str
    message: str
    service: Optional[str]
    severity: Optional[str]
    correlation_id: Optional[str]
    raw: Dict[str, Any]


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        severity=attributes.get("status"),
        correlation_id=(attributes.get("attributes", {}) or {}).get("correlation_id"),
        raw=item,
    )


def normalized_logs_to_json(records: List[NormalizedLogRecord]) -> str:
    return json.dumps([
        {
            "timestamp": record.timestamp,
            "message": record.message,
            "service": record.service,
            "severity": record.severity,
            "correlation_id": record.correlation_id,
        }
        for record in records
    ], indent=2)
