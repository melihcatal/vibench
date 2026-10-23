"""
Local request, response, and normalization helpers for Managed Log Query / Log Ingestion.

Provides data classes and utilities for structuring log events, query parameters,
and normalizing responses from managed logging providers.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    ALERT = "alert"
    EMERGENCY = "emergency"


@dataclass
class StructuredLogEvent:
    """Represents a structured log event ready for ingestion."""

    message: str
    service: str
    environment: str = "production"
    level: LogLevel = LogLevel.INFO
    correlation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None
    hostname: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if self.correlation_id is None:
            self.correlation_id = str(uuid.uuid4())
        if self.hostname is None:
            import socket
            self.hostname = socket.gethostname()
        if not self.tags:
            self.tags = []
        if not self.custom_attributes:
            self.custom_attributes = {}

    def to_datadog_payload(self) -> Dict[str, Any]:
        """Convert to Datadog log event payload format."""
        payload = {
            "ddsource": "python",
            "ddtags": ",".join(self.tags) if self.tags else f"service:{self.service},env:{self.environment}",
            "hostname": self.hostname,
            "service": self.service,
            "message": self.message,
            "status": self.level.value,
            "@timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }
        payload.update(self.custom_attributes)
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_datadog_payload(), default=str)


@dataclass
class LogQueryFilter:
    """Parameters for querying logs from a managed service."""

    query: str = ""
    index: str = "main"
    time_from: Optional[datetime] = None
    time_to: Optional[datetime] = None
    limit: int = 100
    sort: str = "timestamp"
    filter_fields: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_query(self) -> str:
        """Build a Datadog log search query string."""
        parts = []
        if self.query:
            parts.append(self.query)
        for key, value in self.filter_fields.items():
            if isinstance(value, list):
                values_str = " OR ".join(f'@{key}:"{v}"' for v in value)
                parts.append(f"({values_str})")
            else:
                parts.append(f'@{key}:"{value}"')
        if self.time_from and self.time_to:
            from_str = self.time_from.strftime("%Y-%m-%dT%H:%M:%SZ")
            to_str = self.time_to.strftime("%Y-%m-%dT%H:%M:%SZ")
            parts.append(f"timestamp:[{from_str} TO {to_str}]")
        return " ".join(parts) if parts else "*"


@dataclass
class LogEntry:
    """Normalized log entry returned from a query."""

    id: str
    timestamp: str
    message: str
    service: str
    status: str
    correlation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_datadog_response(cls, hit: Dict[str, Any]) -> LogEntry:
        """Create a LogEntry from a Datadog log search result."""
        attributes = hit.get("attributes", {})
        tags = attributes.get("tags", [])
        return cls(
            id=hit.get("id", ""),
            timestamp=attributes.get("timestamp", ""),
            message=attributes.get("message", ""),
            service=attributes.get("service", ""),
            status=attributes.get("status", "unknown"),
            correlation_id=attributes.get("correlation_id"),
            tags=tags,
            attributes={k: v for k, v in attributes.items()
                       if k not in ("message", "service", "status", "tags", "timestamp")},
            raw=hit,
        )


@dataclass
class QueryResult:
    """Container for query results from a managed log service."""

    entries: List[LogEntry]
    total_count: int
    query_string: str
    elapsed_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entries": [asdict(e) for e in self.entries],
            "total_count": self.total_count,
            "query_string": self.query_string,
            "elapsed_ms": self.elapsed_ms,
        }


def generate_correlation_id(prefix: str = "req") -> str:
    """Generate a unique correlation identifier."""
    short_hash = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:12]
    return f"{prefix}-{short_hash}"


def normalize_severity(severity: str) -> LogLevel:
    """Normalize various severity strings to LogLevel enum."""
    severity_map = {
        "debug": LogLevel.DEBUG,
        "info": LogLevel.INFO,
        "information": LogLevel.INFO,
        "notice": LogLevel.NOTICE,
        "warn": LogLevel.WARNING,
        "warning": LogLevel.WARNING,
        "error": LogLevel.ERROR,
        "err": LogLevel.ERROR,
        "critical": LogLevel.CRITICAL,
        "crit": LogLevel.CRITICAL,
        "fatal": LogLevel.CRITICAL,
        "alert": LogLevel.ALERT,
        "emergency": LogLevel.EMERGENCY,
        "emerg": LogLevel.EMERGENCY,
    }
    return severity_map.get(severity.lower().strip(), LogLevel.INFO)


def build_error_query(severity: LogLevel, service: Optional[str] = None,
                      time_window_minutes: int = 60) -> LogQueryFilter:
    """Build a query filter for error-level logs."""
    now = datetime.now(timezone.utc)
    time_from = now.replace(minute=now.minute - time_window_minutes % 60,
                           hour=now.hour - time_window_minutes // 60)
    filter_fields = {"status": severity.value}
    if service:
        filter_fields["service"] = service
    return LogQueryFilter(
        query=f"status:{severity.value}",
        time_from=time_from,
        time_to=now,
        filter_fields=filter_fields,
        limit=50,
    )
