from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum


class LogSeverity(str, Enum):
    """Standard log severity levels."""

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
    """Model for a normalized log entry."""

    timestamp: str
    severity: LogSeverity
    message: str
    service: str
    log_name: Optional[str] = None
    correlation_id: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    structured_data: Dict[str, Any] = field(default_factory=dict)
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = asdict(self)
        result["severity"] = self.severity.value
        return result

    @classmethod
    def from_cloud_logging(cls, entry: Any) -> "LogEntry":
        """
        Create LogEntry from Google Cloud Logging entry.

        Args:
            entry: Google Cloud Logging entry object

        Returns:
            LogEntry instance
        """
        payload = entry.payload if hasattr(entry, "payload") else {}

        # Extract correlation ID from payload or labels
        correlation_id = payload.get("correlation_id") or (
            entry.labels.get("correlation_id") if entry.labels else None
        )

        # Extract service from payload or labels
        service = (
            payload.get("service")
            or (entry.labels.get("service_name") if entry.labels else None)
            or "unknown"
        )

        # Remove known fields from structured data
        structured_data = dict(payload)
        for field_name in [
            "message",
            "service",
            "correlation_id",
            "severity",
            "timestamp",
        ]:
            structured_data.pop(field_name, None)

        return cls(
            timestamp=entry.timestamp.isoformat()
            if entry.timestamp
            else datetime.utcnow().isoformat() + "Z",
            severity=LogSeverity(entry.severity)
            if entry.severity
            else LogSeverity.INFO,
            message=payload.get("message", ""),
            service=service,
            log_name=entry.log_name.split("/")[-1] if entry.log_name else None,
            correlation_id=correlation_id,
            labels=dict(entry.labels) if entry.labels else {},
            structured_data=structured_data,
            resource_type=entry.resource.type if entry.resource else None,
            resource_labels=dict(entry.resource.labels)
            if entry.resource and entry.resource.labels
            else {},
        )


@dataclass
class LogQuery:
    """Model for log query parameters."""

    severity: Optional[LogSeverity] = None
    service_name: Optional[str] = None
    correlation_id: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    hours_back: int = 24
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 100

    def to_cloud_filter(self) -> str:
        """
        Convert to Google Cloud Logging filter string.

        Returns:
            Filter string for Google Cloud Logging
        """
        filter_parts = []

        if self.severity:
            filter_parts.append(f"severity>={self.severity.value}")

        if self.service_name:
            filter_parts.append(f'jsonPayload.service="{self.service_name}"')

        if self.correlation_id:
            filter_parts.append(f'jsonPayload.correlation_id="{self.correlation_id}"')

        for field_name, value in self.field_filters.items():
            if isinstance(value, str):
                filter_parts.append(f'jsonPayload.{field_name}="{value}"')
            else:
                filter_parts.append(f"jsonPayload.{field_name}={value}")

        if self.start_time:
            filter_parts.append(f'timestamp>="{self.start_time}"')

        if self.end_time:
            filter_parts.append(f'timestamp<="{self.end_time}"')

        return " AND ".join(filter_parts) if filter_parts else ""


@dataclass
class LogWriteRequest:
    """Model for writing a log entry."""

    severity: LogSeverity
    message: str
    service_name: str
    log_name: Optional[str] = None
    correlation_id: Optional[str] = None
    structured_data: Dict[str, Any] = field(default_factory=dict)
    labels: Dict[str, str] = field(default_factory=dict)

    def to_cloud_entry(self) -> Dict[str, Any]:
        """
        Convert to Google Cloud Logging entry structure.

        Returns:
            Dictionary for Google Cloud Logging
        """
        entry = {
            "severity": self.severity.value,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "message": self.message,
        }

        if self.correlation_id:
            entry["correlation_id"] = self.correlation_id

        if self.structured_data:
            entry.update(self.structured_data)

        # Build labels
        labels = {
            "environment": "development",  # Would come from env var in real usage
            "service_name": self.service_name,
        }
        labels.update(self.labels)

        return {"entry": entry, "labels": labels}


@dataclass
class QueryResult:
    """Model for query results."""

    query: LogQuery
    entries: List[LogEntry]
    total_count: int
    execution_time: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "query": asdict(self.query),
            "entries": [entry.to_dict() for entry in self.entries],
            "total_count": self.total_count,
            "execution_time": self.execution_time,
        }


def normalize_severity(severity_str: str) -> LogSeverity:
    """
    Normalize a severity string to LogSeverity enum.

    Args:
        severity_str: Severity string

    Returns:
        LogSeverity enum value
    """
    severity_str = severity_str.upper()
    for severity in LogSeverity:
        if severity.value == severity_str:
            return severity

    # Fallback mapping for common variations
    severity_map = {
        "FATAL": LogSeverity.CRITICAL,
        "ERR": LogSeverity.ERROR,
        "WARN": LogSeverity.WARNING,
        "NOTICE": LogSeverity.NOTICE,
        "TRACE": LogSeverity.DEBUG,
        "FINE": LogSeverity.DEBUG,
        "FINER": LogSeverity.DEBUG,
        "FINEST": LogSeverity.DEBUG,
    }

    return severity_map.get(severity_str, LogSeverity.INFO)


def filter_logs_by_severity(
    logs: List[LogEntry], min_severity: LogSeverity
) -> List[LogEntry]:
    """
    Filter logs by minimum severity level.

    Args:
        logs: List of log entries
        min_severity: Minimum severity level

    Returns:
        Filtered list of log entries
    """
    severity_order = {
        LogSeverity.DEBUG: 0,
        LogSeverity.INFO: 1,
        LogSeverity.NOTICE: 2,
        LogSeverity.WARNING: 3,
        LogSeverity.ERROR: 4,
        LogSeverity.CRITICAL: 5,
        LogSeverity.ALERT: 6,
        LogSeverity.EMERGENCY: 7,
    }

    min_level = severity_order[min_severity]
    return [log for log in logs if severity_order.get(log.severity, 0) >= min_level]


def group_logs_by_correlation(logs: List[LogEntry]) -> Dict[str, List[LogEntry]]:
    """
    Group logs by correlation ID.

    Args:
        logs: List of log entries

    Returns:
        Dictionary mapping correlation_id to list of logs
    """
    grouped = {}
    for log in logs:
        if log.correlation_id:
            if log.correlation_id not in grouped:
                grouped[log.correlation_id] = []
            grouped[log.correlation_id].append(log)
    return grouped


def extract_error_patterns(logs: List[LogEntry]) -> List[Dict[str, Any]]:
    """
    Extract common error patterns from log entries.

    Args:
        logs: List of log entries (should be filtered to errors)

    Returns:
        List of error patterns with counts
    """
    error_messages = {}
    for log in logs:
        if log.severity in [LogSeverity.ERROR, LogSeverity.CRITICAL]:
            # Simple pattern extraction - could be enhanced
            message = log.message
            # Remove variable parts like IDs, timestamps
            import re

            cleaned = re.sub(r"\d+", "#", message)
            cleaned = re.sub(r"0x[0-9a-fA-F]+", "HEX", cleaned)
            cleaned = re.sub(
                r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
                "UUID",
                cleaned,
            )

            if cleaned not in error_messages:
                error_messages[cleaned] = {
                    "pattern": cleaned,
                    "original_example": message,
                    "count": 0,
                    "services": set(),
                    "first_seen": log.timestamp,
                    "last_seen": log.timestamp,
                }

            error_messages[cleaned]["count"] += 1
            error_messages[cleaned]["services"].add(log.service)
            error_messages[cleaned]["last_seen"] = max(
                error_messages[cleaned]["last_seen"], log.timestamp
            )
            error_messages[cleaned]["first_seen"] = min(
                error_messages[cleaned]["first_seen"], log.timestamp
            )

    # Convert to list and format
    patterns = []
    for pattern_data in error_messages.values():
        patterns.append(
            {
                "pattern": pattern_data["pattern"],
                "count": pattern_data["count"],
                "services": list(pattern_data["services"]),
                "first_seen": pattern_data["first_seen"],
                "last_seen": pattern_data["last_seen"],
                "example": pattern_data["original_example"],
            }
        )

    return sorted(patterns, key=lambda x: x["count"], reverse=True)
