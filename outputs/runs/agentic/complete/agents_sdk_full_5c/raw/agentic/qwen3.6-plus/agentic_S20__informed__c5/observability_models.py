"""Define local request, response, and normalization helpers for Datadog log operations."""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Any


@dataclass
class StructuredLogEntry:
    """Represents a single structured log event for Datadog Log Intake."""
    message: str
    service: str
    level: str = "info"
    hostname: str = ""
    ddsource: str = "python"
    ddtags: str = ""
    timestamp: Optional[str] = None
    attributes: dict = field(default_factory=dict)

    def to_payload(self) -> dict:
        """Serialize to a Datadog-compatible log payload."""
        payload = {
            "message": self.message,
            "service": self.service,
            "status": self.level,
            "hostname": self.hostname or "unknown",
            "ddsource": self.ddsource,
            "ddtags": self.ddtags,
            "timestamp": self.timestamp or datetime.now(timezone.utc).isoformat(),
        }
        payload.update(self.attributes)
        return payload


@dataclass
class CorrelatedLogEntry:
    """Log event that includes a shared correlation / request ID for trace grouping."""
    message: str
    service: str
    correlation_id: str
    level: str = "info"
    hostname: str = ""
    ddsource: str = "python"
    ddtags: str = ""
    span_id: Optional[str] = None
    trace_id: Optional[str] = None
    timestamp: Optional[str] = None
    attributes: dict = field(default_factory=dict)

    @staticmethod
    def generate_correlation_id() -> str:
        """Generate a UUID-based correlation ID for request tracking."""
        return str(uuid.uuid4())

    def to_payload(self) -> dict:
        """Serialize to a Datadog-compatible log payload with correlation metadata."""
        payload = {
            "message": self.message,
            "service": self.service,
            "status": self.level,
            "hostname": self.hostname or "unknown",
            "ddsource": self.ddsource,
            "ddtags": self.ddtags,
            "timestamp": self.timestamp or datetime.now(timezone.utc).isoformat(),
            "network.client.request_id": self.correlation_id,
            "dd.trace_id": self.trace_id or self.correlation_id.replace("-", ""),
            "dd.span_id": self.span_id or uuid.uuid4().hex[:16],
        }
        payload.update(self.attributes)
        return payload


def normalize_log_response(raw_response: dict) -> list[dict]:
    """Normalize Datadog Logs Query API response into a flat list of log records."""
    results = []
    data = raw_response.get("data", [])
    for event in data:
        attributes = event.get("attributes", {})
        record = {
            "id": event.get("id", ""),
            "timestamp": attributes.get("timestamp", ""),
            "status": attributes.get("status", ""),
            "message": attributes.get("message", ""),
            "service": attributes.get("service", ""),
            "host": attributes.get("host", ""),
        }
        tags = attributes.get("tags", [])
        record["tags"] = tags
        results.append(record)
    return results


def build_error_query(
    service: str,
    environment: str = "",
    extra_filters: list[str] = None,
) -> str:
    """Build a Datadog log query string filtered by severity = error."""
    parts = [f"service:{service}", "status:error"]
    if environment:
        parts.append(f"env:{environment}")
    if extra_filters:
        parts.extend(extra_filters)
    return " AND ".join(parts)


def build_field_query(
    service: str,
    field_filters: dict[str, str] = None,
    environment: str = "",
) -> str:
    """Build a Datadog log query string filtered by arbitrary field values."""
    parts = [f"service:{service}"]
    if environment:
        parts.append(f"env:{environment}")
    if field_filters:
        for key, value in field_filters.items():
            parts.append(f"{key}:{value}")
    return " AND ".join(parts)
