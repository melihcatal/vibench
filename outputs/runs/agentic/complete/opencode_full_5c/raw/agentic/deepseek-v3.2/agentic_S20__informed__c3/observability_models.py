from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class LogSeverity(str, Enum):
    """Log severity levels following Google Cloud Logging conventions."""

    DEFAULT = "DEFAULT"
    DEBUG = "DEBUG"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    ALERT = "ALERT"
    EMERGENCY = "EMERGENCY"


@dataclass
class LogEntry:
    """Model representing a log entry."""

    message: str
    severity: LogSeverity = LogSeverity.INFO
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    component: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary for logging."""
        result = {
            "message": self.message,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat()
            if self.timestamp
            else datetime.utcnow().isoformat(),
        }

        if self.correlation_id:
            result["correlation_id"] = self.correlation_id

        if self.component:
            result["component"] = self.component

        if self.metadata:
            result.update(self.metadata)

        return result


@dataclass
class LogQuery:
    """Model representing a log query."""

    log_name: str
    start_time: datetime
    end_time: datetime
    severity_filter: Optional[LogSeverity] = None
    field_filters: Optional[Dict[str, Any]] = None
    limit: int = 100

    def to_filter_string(self, project_id: str) -> str:
        """Convert query to Google Cloud Logging filter string."""
        from google.cloud.logging_v2._helpers import _datetime_to_rfc3339

        filter_parts = [
            f'logName="projects/{project_id}/logs/{self.log_name}"',
            f'timestamp>="{_datetime_to_rfc3339(self.start_time)}"',
            f'timestamp<="{_datetime_to_rfc3339(self.end_time)}"',
        ]

        if self.severity_filter:
            filter_parts.append(f"severity>={self.severity_filter.value}")

        if self.field_filters:
            for field, value in self.field_filters.items():
                if isinstance(value, str):
                    filter_parts.append(f'jsonPayload.{field}="{value}"')
                else:
                    filter_parts.append(f"jsonPayload.{field}={value}")

        return " AND ".join(filter_parts)


@dataclass
class QueryResult:
    """Model representing query results."""

    entries: List[Dict[str, Any]]
    query: LogQuery
    total_count: int
    execution_time_ms: float

    def get_error_count(self) -> int:
        """Count error severity entries."""
        error_severities = {
            LogSeverity.ERROR.value,
            LogSeverity.CRITICAL.value,
            LogSeverity.ALERT.value,
            LogSeverity.EMERGENCY.value,
        }
        return sum(
            1 for entry in self.entries if entry.get("severity") in error_severities
        )

    def get_by_component(self) -> Dict[str, List[Dict[str, Any]]]:
        """Group entries by component."""
        grouped = {}
        for entry in self.entries:
            payload = entry.get("payload", {})
            component = payload.get("component", "unknown")
            if component not in grouped:
                grouped[component] = []
            grouped[component].append(entry)
        return grouped


@dataclass
class IncidentSummary:
    """Model for incident summary from error logs."""

    incident_id: str
    start_time: datetime
    end_time: datetime
    error_count: int
    affected_components: List[str]
    most_common_error: Optional[str] = None
    sample_errors: List[Dict[str, Any]] = None

    def to_report(self) -> Dict[str, Any]:
        """Convert to report format."""
        return {
            "incident_id": self.incident_id,
            "time_range": {
                "start": self.start_time.isoformat(),
                "end": self.end_time.isoformat(),
            },
            "error_count": self.error_count,
            "affected_components": self.affected_components,
            "most_common_error": self.most_common_error,
            "sample_errors": self.sample_errors or [],
        }


def normalize_cloud_log_entry(entry: Dict[str, Any]) -> LogEntry:
    """Normalize Google Cloud Logging entry to our model."""
    payload = entry.get("payload", {})

    if isinstance(payload, str):
        message = payload
        metadata = {}
    else:
        message = payload.get("message", str(payload))
        metadata = {k: v for k, v in payload.items() if k != "message"}

    return LogEntry(
        message=message,
        severity=LogSeverity(entry.get("severity", "DEFAULT")),
        timestamp=entry.get("timestamp"),
        correlation_id=payload.get("correlation_id")
        if isinstance(payload, dict)
        else None,
        component=payload.get("component") if isinstance(payload, dict) else None,
        metadata=metadata if metadata else None,
        labels=entry.get("labels"),
    )
