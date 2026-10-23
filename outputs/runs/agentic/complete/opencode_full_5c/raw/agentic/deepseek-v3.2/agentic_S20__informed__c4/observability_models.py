from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class LogEntry:
    """Model representing a log entry."""

    timestamp: str
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_cloud_logging(cls, entry: Any) -> "LogEntry":
        """Create LogEntry from Google Cloud Logging entry."""
        payload = entry.payload
        if not isinstance(payload, dict):
            payload = {"raw": str(payload)}

        return cls(
            timestamp=entry.timestamp.isoformat() if entry.timestamp else "",
            severity=entry.severity,
            message=payload.get("message", str(payload)),
            service=entry.resource.labels.get("service", ""),
            correlation_id=entry.labels.get("correlation_id") if entry.labels else None,
            labels=dict(entry.labels) if entry.labels else {},
            payload=payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "service": self.service,
            "correlation_id": self.correlation_id,
            "labels": self.labels,
            "payload": self.payload,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


@dataclass
class LogQuery:
    """Model representing a log query."""

    service_name: Optional[str] = None
    severity_filter: Optional[str] = None
    correlation_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    field_filters: Dict[str, str] = field(default_factory=dict)
    limit: int = 100

    def to_cloud_filter(self) -> str:
        """Convert to Google Cloud Logging filter string."""
        filter_parts = []

        if self.service_name:
            filter_parts.append(f'resource.labels.service="{self.service_name}"')

        if self.severity_filter:
            filter_parts.append(f'severity>="{self.severity_filter}"')

        if self.correlation_id:
            filter_parts.append(f'labels.correlation_id="{self.correlation_id}"')

        if self.start_time:
            filter_parts.append(f'timestamp>="{self.start_time}"')

        if self.end_time:
            filter_parts.append(f'timestamp<="{self.end_time}"')

        for key, value in self.field_filters.items():
            if key in ["severity", "correlation_id"]:
                continue  # Already handled
            filter_parts.append(f'jsonPayload.{key}="{value}"')

        return " AND ".join(filter_parts) if filter_parts else ""


@dataclass
class LogBatch:
    """Model representing a batch of log entries."""

    entries: List[LogEntry] = field(default_factory=list)
    total_count: int = 0
    query: Optional[LogQuery] = None
    fetched_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def add_entry(self, entry: LogEntry):
        """Add a log entry to the batch."""
        self.entries.append(entry)
        self.total_count += 1

    def filter_by_severity(self, min_severity: str) -> "LogBatch":
        """Filter entries by minimum severity."""
        severity_order = {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 2,
            "ERROR": 3,
            "CRITICAL": 4,
        }
        min_level = severity_order.get(min_severity.upper(), 0)

        filtered = []
        for entry in self.entries:
            entry_level = severity_order.get(entry.severity.upper(), 0)
            if entry_level >= min_level:
                filtered.append(entry)

        return LogBatch(
            entries=filtered,
            total_count=len(filtered),
            query=self.query,
            fetched_at=self.fetched_at,
        )

    def get_correlation_groups(self) -> Dict[str, List[LogEntry]]:
        """Group entries by correlation ID."""
        groups = {}
        for entry in self.entries:
            if entry.correlation_id:
                if entry.correlation_id not in groups:
                    groups[entry.correlation_id] = []
                groups[entry.correlation_id].append(entry)
        return groups


@dataclass
class LogSummary:
    """Model representing a summary of log analysis."""

    total_entries: int = 0
    severity_counts: Dict[str, int] = field(default_factory=dict)
    service_counts: Dict[str, int] = field(default_factory=dict)
    unique_correlation_ids: int = 0
    time_range: Optional[str] = None
    error_rate: float = 0.0

    @classmethod
    def from_batch(cls, batch: LogBatch) -> "LogSummary":
        """Create LogSummary from LogBatch."""
        severity_counts = {}
        service_counts = {}
        correlation_ids = set()

        for entry in batch.entries:
            # Count severity
            severity = entry.severity.upper()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Count service
            service_counts[entry.service] = service_counts.get(entry.service, 0) + 1

            # Track correlation IDs
            if entry.correlation_id:
                correlation_ids.add(entry.correlation_id)

        # Calculate error rate
        error_count = severity_counts.get("ERROR", 0) + severity_counts.get(
            "CRITICAL", 0
        )
        error_rate = (error_count / len(batch.entries)) * 100 if batch.entries else 0

        return cls(
            total_entries=len(batch.entries),
            severity_counts=severity_counts,
            service_counts=service_counts,
            unique_correlation_ids=len(correlation_ids),
            time_range=batch.query.to_cloud_filter() if batch.query else None,
            error_rate=error_rate,
        )
