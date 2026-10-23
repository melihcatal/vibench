from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_correlation_id(correlation_id: Optional[str] = None) -> str:
    return correlation_id or str(uuid.uuid4())


@dataclass
class LogEvent:
    message: str
    service: str
    severity: str = "INFO"
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_log(self, ddsource: str = "python", ddtags: Optional[Iterable[str]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.severity.lower(),
            "timestamp": self.timestamp,
            "ddsource": ddsource,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if ddtags:
            payload["ddtags"] = ",".join(ddtags)
        payload.update(self.attributes)
        return payload


@dataclass
class LogQueryWindow:
    start: str
    end: str


@dataclass
class NormalizedLogRecord:
    timestamp: str
    message: str
    service: Optional[str]
    severity: Optional[str]
    correlation_id: Optional[str]
    raw: Dict[str, Any]


@dataclass
class QueryResult:
    records: List[NormalizedLogRecord]
    provider: str = "datadog"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "records": [
                {
                    "timestamp": r.timestamp,
                    "message": r.message,
                    "service": r.service,
                    "severity": r.severity,
                    "correlation_id": r.correlation_id,
                    "raw": r.raw,
                }
                for r in self.records
            ],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def normalize_datadog_log_item(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    return NormalizedLogRecord(
        timestamp=attributes.get("timestamp", ""),
        message=attributes.get("message", ""),
        service=attributes.get("service"),
        severity=attributes.get("status"),
        correlation_id=attributes.get("attributes", {}).get("correlation_id") or attributes.get("correlation_id"),
        raw=item,
    )


def normalize_datadog_search_response(response_json: Dict[str, Any]) -> QueryResult:
    items = response_json.get("data", [])
    return QueryResult(records=[normalize_datadog_log_item(item) for item in items])
