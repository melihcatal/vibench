from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json


ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


@dataclass
class StructuredLogEvent:
    message: str
    service: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        ts = self.timestamp or datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "severity": self.severity.upper(),
            "timestamp": ts.isoformat(),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.attributes)
        return payload


@dataclass
class LogQueryWindow:
    start_time: datetime
    end_time: datetime
    limit: int = 50

    def as_rfc3339(self) -> Dict[str, str]:
        return {
            "start": self.start_time.astimezone(timezone.utc).isoformat(),
            "end": self.end_time.astimezone(timezone.utc).isoformat(),
        }


@dataclass
class NormalizedLogRecord:
    timestamp: str
    severity: str
    message: str
    service: Optional[str]
    correlation_id: Optional[str]
    raw: Dict[str, Any]


def ensure_json_line(event: StructuredLogEvent) -> str:
    return json.dumps(event.to_payload(), separators=(",", ":"), sort_keys=True)


def normalize_datadog_log(item: Dict[str, Any]) -> NormalizedLogRecord:
    attributes = item.get("attributes", {})
    attributes_payload = attributes.get("attributes", {}) if isinstance(attributes, dict) else {}
    message = attributes.get("message") or attributes_payload.get("message") or ""
    service = attributes_payload.get("service") or attributes.get("service")
    correlation_id = (
        attributes_payload.get("correlation_id")
        or attributes_payload.get("request_id")
        or attributes.get("correlation_id")
    )
    severity = (
        attributes_payload.get("severity")
        or attributes.get("status")
        or attributes.get("severity")
        or "UNKNOWN"
    )
    timestamp = attributes.get("timestamp") or ""
    return NormalizedLogRecord(
        timestamp=timestamp,
        severity=str(severity),
        message=str(message),
        service=service,
        correlation_id=correlation_id,
        raw=item,
    )


def summarize_records(records: List[NormalizedLogRecord]) -> Dict[str, Any]:
    severities: Dict[str, int] = {}
    services: Dict[str, int] = {}
    for record in records:
        severities[record.severity] = severities.get(record.severity, 0) + 1
        if record.service:
            services[record.service] = services.get(record.service, 0) + 1
    return {
        "count": len(records),
        "severities": severities,
        "services": services,
    }
