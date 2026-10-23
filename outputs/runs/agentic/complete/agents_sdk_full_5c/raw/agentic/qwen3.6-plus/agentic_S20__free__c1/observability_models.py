"""
Local request, response, and normalization helpers for Datadog Managed Log Query / Log Ingestion.

Defines dataclasses for log events, query filters, and response normalization
utilities specific to the Datadog Logs API v2.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_filter import LogsListRequestFilter
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_list_request_sort import LogsListRequestSort


@dataclass
class StructuredLogEvent:
    """Represents a single structured log event for Datadog ingestion."""
    message: str
    service: str = "default-service"
    env: str = "production"
    status: str = "info"
    ddsource: str = "python"
    hostname: str = "unknown"
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_datadog_payload(self) -> Dict[str, Any]:
        """Convert to a Datadog log submission payload."""
        payload = {
            "message": self.message,
            "ddsource": self.ddsource,
            "service": self.service,
            "env": self.env,
            "status": self.status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": self.hostname,
        }
        if self.attributes:
            payload["ddtags"] = ",".join(
                f"{k}:{v}" for k, v in self.attributes.items() if v is not None
            )
        return payload


@dataclass
class LogQueryFilter:
    """Represents query filters for Datadog log searches."""
    query: str = ""
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    limit: int = 100
    sort: str = "-timestamp"
    indexes: List[str] = field(default_factory=list)

    def to_datadog_filter(self) -> LogsListRequestFilter:
        """Convert to a Datadog LogsListRequestFilter object."""
        time_filter = {}
        if self.from_time:
            time_filter["from"] = self.from_time
        if self.to_time:
            time_filter["to"] = self.to_time
        return LogsListRequestFilter(
            query=self.query,
            indexes=self.indexes if self.indexes else None,
            **time_filter,
        )

    def to_datadog_request(self) -> LogsListRequest:
        """Convert to a full Datadog LogsListRequest object."""
        return LogsListRequest(
            filter=self.to_datadog_filter(),
            page=LogsListRequestPage(limit=self.limit),
            sort=LogsListRequestSort(self.sort),
        )


@dataclass
class LogEntry:
    """Normalized log entry parsed from a Datadog API response."""
    message: str
    status: str
    service: str
    timestamp: str
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_datadog_log_response(response: Dict[str, Any]) -> List[LogEntry]:
    """Parse a Datadog LogsListResponse into a list of normalized LogEntry objects."""
    entries = []
    data = response.get("data", [])
    for item in data:
        attrs = item.get("attributes", {})
        log_attrs = attrs.get("attributes", {})
        entry = LogEntry(
            message=log_attrs.get("message", attrs.get("message", "")),
            status=log_attrs.get("status", attrs.get("status", "unknown")),
            service=log_attrs.get("service", attrs.get("service", "unknown")),
            timestamp=attrs.get("timestamp", ""),
            correlation_id=log_attrs.get("correlation_id"),
            attributes=log_attrs,
            raw=item,
        )
        entries.append(entry)
    return entries


@dataclass
class IncidentSummary:
    """Summarized incident findings from log analysis."""
    incident_id: str
    total_errors: int
    affected_services: List[str] = field(default_factory=list)
    error_messages: List[str] = field(default_factory=list)
    time_range: Dict[str, str] = field(default_factory=dict)
    correlation_ids: List[str] = field(default_factory=list)

    def to_report(self) -> Dict[str, Any]:
        """Return a dictionary representation for incident review."""
        return {
            "incident_id": self.incident_id,
            "total_errors": self.total_errors,
            "affected_services": list(set(self.affected_services)),
            "error_messages": self.error_messages,
            "time_range": self.time_range,
            "unique_correlation_ids": len(set(self.correlation_ids)),
            "correlation_ids_sample": list(set(self.correlation_ids))[:10],
        }
