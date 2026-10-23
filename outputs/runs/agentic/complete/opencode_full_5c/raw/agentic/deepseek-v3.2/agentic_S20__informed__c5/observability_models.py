from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class LogSeverity(str, Enum):
    """Log severity levels."""

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
    """Model for a log entry."""

    timestamp: str
    severity: LogSeverity
    message: str
    service: Optional[str] = None
    component: Optional[str] = None
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        result = {
            "timestamp": self.timestamp,
            "severity": self.severity.value,
            "message": self.message,
        }

        if self.service:
            result["service"] = self.service
        if self.component:
            result["component"] = self.component
        if self.correlation_id:
            result["correlation_id"] = self.correlation_id
        if self.metadata:
            result.update(self.metadata)

        return result

    @classmethod
    def from_cloud_entry(cls, entry_data: Dict[str, Any]) -> "LogEntry":
        """Create LogEntry from cloud logging entry."""
        payload = entry_data.get("payload", {})

        return cls(
            timestamp=entry_data.get("timestamp", ""),
            severity=LogSeverity(entry_data.get("severity", "INFO")),
            message=payload.get("message", "")
            if isinstance(payload, dict)
            else str(payload),
            service=payload.get("service") if isinstance(payload, dict) else None,
            component=payload.get("component") if isinstance(payload, dict) else None,
            correlation_id=payload.get("correlation_id")
            if isinstance(payload, dict)
            else None,
            metadata=payload if isinstance(payload, dict) else {"raw": str(payload)},
        )


@dataclass
class LogQuery:
    """Model for log query parameters."""

    start_time: datetime
    end_time: datetime
    severity_filter: Optional[LogSeverity] = None
    service_filter: Optional[str] = None
    component_filter: Optional[str] = None
    correlation_id_filter: Optional[str] = None
    limit: int = 100

    def to_filter_string(self) -> str:
        """Convert to Google Cloud Logging filter string."""
        filters = []

        filters.append(f'timestamp >= "{self.start_time.isoformat()}Z"')
        filters.append(f'timestamp <= "{self.end_time.isoformat()}Z"')

        if self.severity_filter:
            filters.append(f'severity = "{self.severity_filter.value}"')

        if self.service_filter:
            filters.append(f'jsonPayload.service = "{self.service_filter}"')

        if self.component_filter:
            filters.append(f'jsonPayload.component = "{self.component_filter}"')

        if self.correlation_id_filter:
            filters.append(
                f'jsonPayload.correlation_id = "{self.correlation_id_filter}"'
            )

        return " AND ".join(filters)


@dataclass
class LogBatch:
    """Model for a batch of log entries."""

    entries: List[LogEntry]
    query_time: datetime
    total_count: int

    def get_by_severity(self, severity: LogSeverity) -> List[LogEntry]:
        """Filter entries by severity."""
        return [entry for entry in self.entries if entry.severity == severity]

    def get_errors(self) -> List[LogEntry]:
        """Get all error entries."""
        error_severities = [
            LogSeverity.ERROR,
            LogSeverity.CRITICAL,
            LogSeverity.ALERT,
            LogSeverity.EMERGENCY,
        ]
        return [entry for entry in self.entries if entry.severity in error_severities]

    def get_unique_correlation_ids(self) -> List[str]:
        """Get unique correlation IDs from the batch."""
        ids = set()
        for entry in self.entries:
            if entry.correlation_id:
                ids.add(entry.correlation_id)
        return list(ids)


class LogNormalizer:
    """Helper for normalizing log data across different sources."""

    @staticmethod
    def normalize_severity(severity: str) -> LogSeverity:
        """Normalize severity string to LogSeverity enum."""
        severity_upper = severity.upper()

        severity_map = {
            "DEBUG": LogSeverity.DEBUG,
            "INFO": LogSeverity.INFO,
            "NOTICE": LogSeverity.NOTICE,
            "WARN": LogSeverity.WARNING,
            "WARNING": LogSeverity.WARNING,
            "ERR": LogSeverity.ERROR,
            "ERROR": LogSeverity.ERROR,
            "CRIT": LogSeverity.CRITICAL,
            "CRITICAL": LogSeverity.CRITICAL,
            "ALERT": LogSeverity.ALERT,
            "EMERG": LogSeverity.EMERGENCY,
            "EMERGENCY": LogSeverity.EMERGENCY,
        }

        return severity_map.get(severity_upper, LogSeverity.INFO)

    @staticmethod
    def extract_correlation_id(payload: Dict[str, Any]) -> Optional[str]:
        """Extract correlation ID from log payload."""
        correlation_fields = [
            "correlation_id",
            "correlationId",
            "request_id",
            "requestId",
            "trace_id",
            "traceId",
        ]

        for field in correlation_fields:
            if field in payload:
                value = payload[field]
                if isinstance(value, str) and value.strip():
                    return value.strip()

        return None

    @staticmethod
    def format_timestamp(timestamp: Any) -> str:
        """Format timestamp to ISO format."""
        if isinstance(timestamp, datetime):
            return timestamp.isoformat() + "Z"
        elif isinstance(timestamp, str):
            return timestamp
        else:
            return datetime.utcnow().isoformat() + "Z"
