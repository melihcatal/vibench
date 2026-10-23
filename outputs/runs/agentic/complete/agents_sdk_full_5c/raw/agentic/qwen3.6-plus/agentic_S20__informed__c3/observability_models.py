"""
Local request, response, and normalization helpers for Managed Log Query / Log Ingestion.
Supports Datadog Logs API payload structures and response parsing.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class LogEvent:
    """Represents a structured log event for ingestion."""
    message: str
    hostname: str = "localhost"
    service: str = "default-service"
    status: str = "info"
    ddsource: str = "python"
    ddtags: str = ""
    timestamp: Optional[int] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

    def to_datadog_payload(self) -> Dict[str, Any]:
        """Convert to Datadog Logs API ingestion format."""
        payload = {
            "ddsource": self.ddsource,
            "ddtags": self.ddtags,
            "hostname": self.hostname,
            "message": self.message,
            "service": self.service,
            "status": self.status,
        }
        if self.timestamp:
            payload["timestamp"] = self.timestamp
        else:
            payload["timestamp"] = int(datetime.now(timezone.utc).timestamp() * 1000)
        merged_attrs = dict(self.attributes)
        if self.correlation_id:
            merged_attrs["correlation_id"] = self.correlation_id
        if merged_attrs:
            payload.update(merged_attrs)
        return payload

    @staticmethod
    def generate_correlation_id() -> str:
        """Generate a UUID-based correlation identifier."""
        return str(uuid.uuid4())


@dataclass
class LogQueryRequest:
    """Represents a query for fetching logs from Datadog."""
    query: str = ""
    time_from: Optional[int] = None
    time_to: Optional[int] = None
    limit: int = 100
    sort: str = "timestamp"

    def to_datadog_params(self) -> Dict[str, Any]:
        """Convert to Datadog Logs API query parameters."""
        params = {
            "filter[query]": self.query,
            "filter[limit]": self.limit,
            "sort": self.sort,
        }
        if self.time_from:
            params["filter[from]"] = datetime.fromtimestamp(
                self.time_from, tz=timezone.utc
            ).isoformat()
        if self.time_to:
            params["filter[to]"] = datetime.fromtimestamp(
                self.time_to, tz=timezone.utc
            ).isoformat()
        return params


@dataclass
class LogEntry:
    """Normalized log entry parsed from a Datadog API response."""
    message: str
    status: str
    timestamp: Optional[int] = None
    hostname: Optional[str] = None
    service: Optional[str] = None
    correlation_id: Optional[str] = None
    raw_attributes: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_datadog_response(cls, datum: Dict[str, Any]) -> "LogEntry":
        """Parse a single log entry from Datadog Logs API response."""
        attributes = datum.get("attributes", {})
        return cls(
            message=attributes.get("message", ""),
            status=attributes.get("status", "info"),
            timestamp=attributes.get("timestamp"),
            hostname=attributes.get("hostname"),
            service=attributes.get("service"),
            correlation_id=attributes.get("correlation_id"),
            raw_attributes=attributes,
        )


@dataclass
class LogQueryResponse:
    """Container for parsed log query results."""
    entries: List[LogEntry] = field(default_factory=list)
    total_count: int = 0
    next_page_token: Optional[str] = None

    @classmethod
    def from_datadog_response(cls, response_data: Dict[str, Any]) -> "LogQueryResponse":
        """Parse a full Datadog Logs API response into normalized entries."""
        data_list = response_data.get("data", [])
        entries = [LogEntry.from_datadog_response(d) for d in data_list]
        meta = response_data.get("meta", {})
        return cls(
            entries=entries,
            total_count=meta.get("page", {}).get("total", len(entries)),
            next_page_token=meta.get("page", {}).get("after"),
        )
