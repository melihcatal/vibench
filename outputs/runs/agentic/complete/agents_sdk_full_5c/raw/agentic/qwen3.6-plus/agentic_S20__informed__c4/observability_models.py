"""
Local request, response, and normalization helpers for Managed Log Query / Log Ingestion.

Defines data models and parsing utilities used across Datadog log ingestion and query operations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class LogEvent:
    """Represents a structured log event for ingestion into Datadog."""
    message: str
    service: str = "default"
    status: str = "info"
    hostname: str = ""
    ddsource: str = "python"
    ddtags: str = ""
    attributes: dict = field(default_factory=dict)
    timestamp: Optional[str] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if not self.hostname:
            import socket
            try:
                self.hostname = socket.gethostname()
            except Exception:
                self.hostname = "unknown"


def normalize_log_event(event: LogEvent) -> dict:
    """Normalize a LogEvent into a Datadog-compatible ingestion payload.

    Datadog expects a flat JSON structure with specific top-level keys:
    ddsource, ddtags, hostname, message, service, status, timestamp,
    plus any custom attributes merged at the top level.
    """
    payload = {
        "ddsource": event.ddsource,
        "ddtags": event.ddtags,
        "hostname": event.hostname,
        "message": event.message,
        "service": event.service,
        "status": event.status,
        "timestamp": event.timestamp,
    }
    payload.update(event.attributes)
    return payload


@dataclass
class LogQueryParams:
    """Parameters for querying logs from Datadog."""
    query_string: str = "status:error"
    from_minutes_ago: int = 60
    to_minutes_ago: int = 0
    page_size: int = 25
    sort_order: str = "-timestamp"
    cursor: Optional[str] = None
    additional_filters: dict = field(default_factory=dict)


@dataclass
class ParsedLogEntry:
    """A normalized log entry returned from a query."""
    timestamp: str
    message: str
    status: str
    service: str
    hostname: str
    correlation_id: Optional[str] = None
    raw_attributes: dict = field(default_factory=dict)
    event_id: Optional[str] = None


def parse_datadog_log_entry(entry: dict) -> ParsedLogEntry:
    """Parse a raw Datadog log event response into a normalized ParsedLogEntry.

    Datadog v2 Logs API returns events with nested structure:
    data[].attributes contains timestamp, message, service, tags, status, etc.
    """
    attrs = entry.get("attributes", {})
    attributes = entry.get("attributes", {})

    # Extract timestamp - Datadog returns it as epoch milliseconds or ISO string
    ts = attributes.get("timestamp", "")
    if isinstance(ts, (int, float)):
        ts = datetime.fromtimestamp(ts / 1000, tz=timezone.utc).isoformat()

    return ParsedLogEntry(
        timestamp=ts,
        message=attributes.get("message", ""),
        status=attributes.get("status", "unknown"),
        service=attributes.get("service", ""),
        hostname=attributes.get("host", {}).get("name", ""),
        correlation_id=attributes.get("correlation_id", None),
        raw_attributes=attributes,
        event_id=entry.get("id", None),
    )


@dataclass
class LogQueryResponse:
    """Container for paginated query results."""
    logs: list[ParsedLogEntry] = field(default_factory=list)
    cursor: Optional[str] = None
    total_count: int = 0

    @property
    def has_more(self) -> bool:
        return self.cursor is not None
