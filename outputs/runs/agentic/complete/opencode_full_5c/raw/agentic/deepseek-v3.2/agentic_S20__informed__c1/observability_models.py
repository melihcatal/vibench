from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class LogSeverity(str, Enum):
    """Standard log severity levels."""

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
    severity: LogSeverity
    timestamp: datetime
    service_name: str
    log_name: str = "application-logs"
    correlation_id: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    resource_type: str = "global"
    resource_labels: Optional[Dict[str, str]] = None
    extra_fields: Optional[Dict[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        """Convert to payload dictionary for logging."""
        payload = {
            "message": self.message,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
            "service": self.service_name,
            "log_name": self.log_name,
        }

        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id

        if self.extra_fields:
            payload.update(self.extra_fields)

        return payload

    def to_cloud_logging_format(self) -> Dict[str, Any]:
        """Format for Google Cloud Logging."""
        return {
            "log_name": self.log_name,
            "resource": {
                "type": self.resource_type,
                "labels": self.resource_labels or {},
            },
            "severity": self.severity.value,
            "labels": self.labels or {},
            "payload": self.to_payload(),
        }


@dataclass
class LogQuery:
    """Model representing a log query."""

    start_time: datetime
    end_time: datetime
    severity_filter: Optional[LogSeverity] = None
    service_filter: Optional[str] = None
    log_name_filter: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    limit: int = 100
    order_by: str = "timestamp desc"

    def to_cloud_logging_filter(self) -> str:
        """Convert to Cloud Logging filter syntax."""
        query_parts = [
            f'timestamp>="{self.start_time.isoformat()}Z"',
            f'timestamp<="{self.end_time.isoformat()}Z"',
        ]

        if self.severity_filter:
            query_parts.append(f'severity="{self.severity_filter.value}"')

        if self.service_filter:
            query_parts.append(f'resource.labels.service="{self.service_filter}"')

        if self.log_name_filter:
            query_parts.append(f'logName="{self.log_name_filter}"')

        if self.field_filters:
            for field, value in self.field_filters.items():
                if isinstance(value, str):
                    query_parts.append(f'{field}="{value}"')
                else:
                    query_parts.append(f"{field}={value}")

        return " AND ".join(query_parts)

    @classmethod
    def create_recent_query(cls, minutes: int = 30, **kwargs) -> "LogQuery":
        """Create a query for recent logs."""
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=minutes)
        return cls(start_time=start_time, end_time=end_time, **kwargs)


@dataclass
class QueryResult:
    """Model representing query results."""

    query: LogQuery
    total_results: int
    results: List[Dict[str, Any]]
    severity_distribution: Dict[str, int]
    execution_time_ms: float

    def to_summary(self) -> Dict[str, Any]:
        """Create a summary of the query results."""
        return {
            "query_filter": self.query.to_cloud_logging_filter(),
            "time_range": {
                "start": self.query.start_time.isoformat(),
                "end": self.query.end_time.isoformat(),
            },
            "total_logs": self.total_results,
            "severity_breakdown": self.severity_distribution,
            "execution_time_ms": self.execution_time_ms,
        }

    def get_error_logs(self) -> List[Dict[str, Any]]:
        """Get only error and higher severity logs."""
        error_severities = [
            LogSeverity.ERROR,
            LogSeverity.CRITICAL,
            LogSeverity.ALERT,
            LogSeverity.EMERGENCY,
        ]
        error_severity_values = [sev.value for sev in error_severities]

        return [
            log for log in self.results if log.get("severity") in error_severity_values
        ]


@dataclass
class CorrelationBatch:
    """Model for correlated log batches."""

    correlation_id: str
    service_name: str
    logs: List[LogEntry]
    start_time: datetime
    end_time: Optional[datetime] = None

    def add_log(self, log: LogEntry):
        """Add a log to the batch."""
        if log.correlation_id != self.correlation_id:
            raise ValueError(
                f"Log correlation_id {log.correlation_id} doesn't match batch {self.correlation_id}"
            )

        self.logs.append(log)

        # Update end time
        if self.end_time is None or log.timestamp > self.end_time:
            self.end_time = log.timestamp

    def get_duration_seconds(self) -> Optional[float]:
        """Get duration of the correlation batch in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def to_sequence_payloads(self) -> List[Dict[str, Any]]:
        """Convert logs to sequence-numbered payloads."""
        payloads = []
        for i, log in enumerate(self.logs):
            payload = log.to_payload()
            payload["sequence"] = i + 1
            payload["total_sequences"] = len(self.logs)
            payloads.append(payload)
        return payloads


# Helper functions
def normalize_timestamp(timestamp_str: str) -> datetime:
    """Normalize timestamp string to datetime."""
    if timestamp_str.endswith("Z"):
        timestamp_str = timestamp_str[:-1] + "+00:00"
    return datetime.fromisoformat(timestamp_str)


def parse_cloud_logging_entry(entry_data: Dict[str, Any]) -> LogEntry:
    """Parse Cloud Logging entry data into LogEntry model."""
    # Extract timestamp
    timestamp_str = entry_data.get("timestamp")
    if timestamp_str:
        timestamp = normalize_timestamp(timestamp_str)
    else:
        timestamp = datetime.utcnow()

    # Extract severity
    severity_str = entry_data.get("severity", "DEFAULT")
    try:
        severity = LogSeverity(severity_str)
    except ValueError:
        severity = LogSeverity.DEFAULT

    # Extract message
    payload = entry_data.get("payload", {})
    if isinstance(payload, dict):
        message = payload.get("message", str(payload))
    else:
        message = str(payload)

    # Extract service name from resource labels or payload
    service_name = "unknown-service"
    resource_labels = entry_data.get("resource_labels", {})
    if "service" in resource_labels:
        service_name = resource_labels["service"]
    elif isinstance(payload, dict) and "service" in payload:
        service_name = payload["service"]

    # Extract correlation ID
    correlation_id = None
    if isinstance(payload, dict) and "correlation_id" in payload:
        correlation_id = payload["correlation_id"]

    # Extract extra fields
    extra_fields = {}
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key not in [
                "message",
                "service",
                "correlation_id",
                "severity",
                "timestamp",
            ]:
                extra_fields[key] = value

    return LogEntry(
        message=message,
        severity=severity,
        timestamp=timestamp,
        service_name=service_name,
        log_name=entry_data.get("log_name", "application-logs"),
        correlation_id=correlation_id,
        labels=entry_data.get("labels"),
        resource_type=entry_data.get("resource_type", "global"),
        resource_labels=resource_labels,
        extra_fields=extra_fields if extra_fields else None,
    )


# Import timedelta for the create_recent_query method
from datetime import timedelta
