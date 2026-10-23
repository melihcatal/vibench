"""Local request, response, and normalization helpers for Managed Log Query / Log Ingestion."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    """Represents a structured log event to be written."""
    severity: str
    message: str
    service_name: str
    timestamp: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    http_request: Optional[Dict[str, Any]] = None
    json_payload: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None

    def to_google_cloud_logging_entry(self) -> Dict[str, Any]:
        """Convert to a Google Cloud Logging LogEntry payload format."""
        severity_map = {
            "DEBUG": "DEBUG",
            "INFO": "INFO",
            "NOTICE": "NOTICE",
            "WARNING": "WARNING",
            "ERROR": "ERROR",
            "CRITICAL": "CRITICAL",
            "ALERT": "ALERT",
            "EMERGENCY": "EMERGENCY",
        }
        entry = {
            "severity": severity_map.get(self.severity.upper(), "DEFAULT"),
            "textPayload": self.message,
            "timestamp": (self.timestamp or datetime.now(timezone.utc)).isoformat(),
            "labels": dict(self.labels),
            "serviceContext": {
                "service": self.service_name,
            },
        }
        if self.trace_id:
            entry["trace"] = self.trace_id
        if self.span_id:
            entry["spanId"] = self.span_id
        if self.correlation_id:
            entry["labels"]["correlation_id"] = self.correlation_id
        if self.http_request:
            entry["httpRequest"] = self.http_request
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
        return entry


@dataclass
class LogQueryRequest:
    """Represents a query against a managed logging service."""
    filter_expression: str
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None
    max_results: int = 100
    order_by: str = "timestamp desc"


@dataclass
class LogEntry:
    """Normalized log entry returned from query results."""
    timestamp: datetime
    severity: str
    message: str
    resource_type: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    raw_entry: Optional[Dict[str, Any]] = None

    @classmethod
    def from_google_cloud_logging_entry(cls, entry: Dict[str, Any]) -> "LogEntry":
        """Parse a Google Cloud Logging entry dict into a normalized LogEntry."""
        timestamp = entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            ts = datetime.now(timezone.utc)

        labels = entry.get("labels", {})
        if isinstance(labels, dict):
            labels = dict(labels)
        else:
            labels = {}

        return cls(
            timestamp=ts,
            severity=entry.get("severity", "DEFAULT"),
            message=entry.get("textPayload", entry.get("jsonPayload", {})),
            resource_type=entry.get("resource", {}).get("type", ""),
            labels=labels,
            trace_id=entry.get("trace"),
            correlation_id=labels.get("correlation_id"),
            raw_entry=entry,
        )


@dataclass
class LogQueryResponse:
    """Normalized response from a log query."""
    entries: List[LogEntry]
    total_count: int = 0
    next_page_token: Optional[str] = None
