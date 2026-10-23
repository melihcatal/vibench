"""
Local request, response, and normalization helpers for Managed Log Query / Log Ingestion.

Provides data models, payload builders, and response parsers for log ingestion
and querying workflows.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    """Represents a single structured log event."""

    message: str
    status: str = "info"
    service: str = "default-service"
    source: str = "python-app"
    ddsource: str = "python"
    ddtags: str = "env:production"
    correlation_id: Optional[str] = None
    hostname: str = "localhost"
    timestamp: Optional[float] = None
    custom_attributes: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        """Serialize the log event into a JSON payload compatible with Datadog."""
        ts = self.timestamp or datetime.now(timezone.utc).timestamp()
        payload = {
            "ddsource": self.ddsource,
            "ddtags": self.ddtags,
            "hostname": self.hostname,
            "message": self.message,
            "service": self.service,
            "status": self.status.lower(),
            "timestamp": int(ts * 1000),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        payload.update(self.custom_attributes)
        return payload


@dataclass
class LogQueryRequest:
    """Parameters for a log search query."""

    query: str
    time_from: datetime
    time_to: datetime
    limit: int = 50
    sort: str = "timestamp"
    indices: Optional[List[str]] = None
    filter_query: Optional[str] = None

    def to_datadog_payload(self) -> Dict[str, Any]:
        """Build the Datadog v2 logs search API request body."""
        payload: Dict[str, Any] = {
            "filter": {
                "query": self.query,
                "from": self.time_from.isoformat(),
                "to": self.time_to.isoformat(),
            },
            "sort": self.sort,
            "page": {
                "limit": self.limit,
            },
        }
        if self.indices:
            payload["filter"]["indices"] = self.indices
        if self.filter_query:
            payload["filter"]["query"] = self.filter_query
        return payload


@dataclass
class ParsedLogEntry:
    """Normalized log entry returned from a query response."""

    message: str
    status: str
    service: str
    timestamp: datetime
    correlation_id: Optional[str] = None
    raw_attributes: Dict[str, Any] = field(default_factory=dict)
    log_id: Optional[str] = None

    @classmethod
    def from_datadog_response(cls, event: Dict[str, Any]) -> "ParsedLogEntry":
        """Parse a single Datadog log event into a normalized entry."""
        attributes = event.get("attributes", {})
        tags = attributes.get("tags", [])
        status = attributes.get("status", "unknown")
        service = attributes.get("service", "unknown")
        timestamp_str = attributes.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            ts = datetime.now(timezone.utc)

        correlation_id = attributes.get("correlation_id")
        message = attributes.get("message", "")
        log_id = event.get("id")

        return cls(
            message=message,
            status=status,
            service=service,
            timestamp=ts,
            correlation_id=correlation_id,
            raw_attributes=attributes,
            log_id=log_id,
        )


@dataclass
class LogQueryResponse:
    """Parsed response from a log query."""

    entries: List[ParsedLogEntry]
    total_count: int = 0
    next_page_token: Optional[str] = None

    @classmethod
    def from_datadog_response(cls, response_body: Dict[str, Any]) -> "LogQueryResponse":
        """Parse Datadog v2 logs search response into normalized entries."""
        data = response_body.get("data", [])
        entries = [ParsedLogEntry.from_datadog_response(event) for event in data]
        meta = response_body.get("meta", {})
        pagination = meta.get("page", {})
        total = pagination.get("total_matched", 0)
        next_token = pagination.get("after")
        return cls(
            entries=entries,
            total_count=total,
            next_page_token=next_token,
        )


def generate_correlation_id() -> str:
    """Generate a unique correlation ID for request tracing."""
    return str(uuid.uuid4())


def format_time_window(minutes_ago: int = 30) -> tuple[datetime, datetime]:
    """Return a (from, to) datetime tuple for recent time range queries."""
    now = datetime.now(timezone.utc)
    time_from = datetime.fromtimestamp(
        now.timestamp() - minutes_ago * 60, tz=timezone.utc
    )
    return time_from, now


def severity_filter(severity: str) -> str:
    """Return a Datadog query filter string for a given severity level."""
    severity_map = {
        "error": "status:error",
        "warn": "status:warn",
        "warning": "status:warn",
        "info": "status:info",
        "debug": "status:debug",
        "critical": "status:critical OR status:error",
    }
    return severity_map.get(severity.lower(), f"status:{severity}")
