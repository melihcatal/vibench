"""Local request, response, and normalization helpers for Managed Log Query / Log Ingestion.

Provider: Datadog Log Management (https://docs.datadoghq.com/logs/)
"""

import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, Any


@dataclass
class StructuredLogEvent:
    """Represents a single structured log event for Datadog ingestion."""

    message: str
    service: str
    status: str = "INFO"
    source: str = "python-app"
    hostname: Optional[str] = None
    timestamp: Optional[str] = None
    ddtags: str = ""
    extra_attributes: dict = field(default_factory=dict)

    def to_datadog_payload(self) -> dict:
        """Normalize the log event into a Datadog-compatible JSON payload.

        Datadog log intake accepts a JSON object with specific top-level keys.
        Reference: https://docs.datadoghq.com/api/latest/logs/#send-logs
        """
        payload = {
            "message": self.message,
            "service": self.service,
            "status": self.status.upper(),
            "source": self.source,
            "ddtags": self.ddtags,
        }
        if self.hostname:
            payload["hostname"] = self.hostname
        if self.timestamp:
            payload["timestamp"] = self.timestamp
        else:
            payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        payload.update(self.extra_attributes)
        return payload


@dataclass
class CorrelatedLogEvent(StructuredLogEvent):
    """A log event enriched with correlation/trace identifiers for request tracing."""

    correlation_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    request_path: Optional[str] = None
    request_method: Optional[str] = None

    def to_datadog_payload(self) -> dict:
        """Normalize with Datadog trace correlation fields.

        Datadog uses specific field names for APM correlation:
        - dd.trace_id
        - dd.span_id
        """
        payload = super().to_datadog_payload()
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.trace_id:
            payload["dd.trace_id"] = self.trace_id
        if self.span_id:
            payload["dd.span_id"] = self.span_id
        if self.request_path:
            payload["http.url"] = self.request_path
        if self.request_method:
            payload["http.method"] = self.request_method
        return payload


@dataclass
class LogQueryRequest:
    """Represents a log query request for the Datadog Logs API.

    Reference: https://docs.datadoghq.com/api/latest/logs/#search-logs
    """

    query: str = ""
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    limit: int = 25
    sort: str = "timestamp"
    fields: list = field(default_factory=list)

    def to_datadog_body(self) -> dict:
        """Convert to Datadog Logs API v2 request body."""
        body: dict[str, Any] = {
            "data": {
                "attributes": {
                    "query": self.query,
                    "sort": self.sort,
                    "page": {
                        "limit": self.limit,
                    },
                }
            }
        }
        if self.time_from or self.time_to:
            time_filter: dict[str, Any] = {}
            if self.time_from:
                time_filter["from"] = self.time_from
            if self.time_to:
                time_filter["to"] = self.time_to
            body["data"]["attributes"]["time"] = time_filter
        if self.fields:
            body["data"]["attributes"]["fields"] = self.fields
        return body


@dataclass
class LogQueryResponse:
    """Parsed response from a Datadog log query."""

    logs: list[dict] = field(default_factory=list)
    next_page_token: Optional[str] = None
    total_count: int = 0
    status: str = "ok"
    raw_response: Optional[dict] = None

    @classmethod
    def from_datadog_response(cls, response_body: dict) -> "LogQueryResponse":
        """Parse a Datadog Logs API v2 response into normalized form."""
        logs = []
        data = response_body.get("data", [])
        for item in data:
            attrs = item.get("attributes", {})
            logs.append(attrs)
        next_page = None
        links = response_body.get("links", {})
        if links.get("next"):
            next_page = links["next"].split("page[after]=")[-1] if "page[after]=" in links.get("next", "") else None
        total = response_body.get("meta", {}).get("page", {}).get("total", 0)
        return cls(
            logs=logs,
            next_page_token=next_page,
            total_count=total,
            status=response_body.get("status", "ok"),
            raw_response=response_body,
        )


def generate_correlation_id() -> str:
    """Generate a UUID-based correlation ID for request tracing."""
    return str(uuid.uuid4())


def generate_trace_id() -> str:
    """Generate a 64-bit trace ID compatible with Datadog APM."""
    return str(uuid.getnode() % (2**64))


def generate_span_id() -> str:
    """Generate a 64-bit span ID compatible with Datadog APM."""
    import random
    return str(random.getrandbits(64))


def build_error_query(service: str, hours: int = 1) -> str:
    """Build a Datadog log search query for error-level logs.

    Datadog uses Lucene-style query syntax.
    Reference: https://docs.datadoghq.com/logs/explorer/search_syntax/
    """
    return f"status:error service:{service}"


def build_recent_query(service: str, field_filter: Optional[dict] = None) -> str:
    """Build a Datadog log search query for recent logs with optional field filters."""
    parts = [f"service:{service}"]
    if field_filter:
        for key, value in field_filter.items():
            parts.append(f"{key}:{value}")
    return " ".join(parts)
