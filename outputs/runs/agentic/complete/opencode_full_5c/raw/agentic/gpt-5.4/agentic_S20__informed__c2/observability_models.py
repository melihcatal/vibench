from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_correlation_id(value: str | None = None) -> str:
    return value or str(uuid.uuid4())


def _compact(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _compact(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_compact(v) for v in value if v is not None]
    return value


@dataclass
class StructuredLogEvent:
    message: str
    severity: str
    service: str
    environment: str
    timestamp: str = field(default_factory=utc_now_iso)
    correlation_id: str | None = None
    request_id: str | None = None
    logger_name: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    labels: dict[str, str] = field(default_factory=dict)
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.upper()
        payload["correlation_id"] = ensure_correlation_id(self.correlation_id)
        return _compact(payload)

    def to_json(self) -> str:
        return json.dumps(self.to_payload(), separators=(",", ":"), sort_keys=True)


@dataclass
class LogQueryWindow:
    start_time: datetime
    end_time: datetime

    def to_rfc3339(self) -> tuple[str, str]:
        return self.start_time.astimezone(
            timezone.utc
        ).isoformat(), self.end_time.astimezone(timezone.utc).isoformat()


@dataclass
class LogQueryResult:
    timestamp: str
    severity: str
    message: str
    correlation_id: str | None
    service: str | None
    raw: dict[str, Any]


def normalize_cloudwatch_results(
    results: list[list[dict[str, str]]],
) -> list[LogQueryResult]:
    normalized: list[LogQueryResult] = []
    for row in results:
        values = {item.get("field", ""): item.get("value") for item in row}
        normalized.append(
            LogQueryResult(
                timestamp=values.get("@timestamp", ""),
                severity=values.get("severity", values.get("level", "")),
                message=values.get("message", values.get("@message", "")),
                correlation_id=values.get("correlation_id") or values.get("request_id"),
                service=values.get("service"),
                raw=values,
            )
        )
    return normalized
