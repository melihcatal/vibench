from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json


@dataclass
class LogEntry:
    message: str
    severity: str
    timestamp: datetime
    labels: Dict[str, str]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    resource: Optional[Dict[str, Any]] = None

    @classmethod
    def from_cloud_logging_entry(cls, entry) -> "LogEntry":
        """Convert Google Cloud Logging entry to LogEntry model."""
        payload = entry.payload
        if isinstance(payload, dict):
            message = payload.get("message", str(payload))
        else:
            message = str(payload)

        return cls(
            message=message,
            severity=entry.severity,
            timestamp=entry.timestamp,
            labels=entry.labels or {},
            trace_id=entry.trace if hasattr(entry, "trace") else None,
            span_id=entry.span_id if hasattr(entry, "span_id") else None,
            resource=entry.resource.to_api_repr() if entry.resource else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "labels": self.labels,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "resource": self.resource,
        }


@dataclass
class LogQuery:
    severity_filter: Optional[str] = None
    time_range_hours: int = 24
    label_filters: Optional[Dict[str, str]] = None
    text_search: Optional[str] = None

    def to_cloud_logging_filter(self) -> str:
        """Convert to Google Cloud Logging filter string."""
        filters = []

        if self.severity_filter:
            filters.append(f'severity="{self.severity_filter}"')

        if self.time_range_hours:
            time_cutoff = datetime.utcnow() - timedelta(hours=self.time_range_hours)
            filters.append(f'timestamp>="{time_cutoff.isoformat()}"')

        if self.label_filters:
            for key, value in self.label_filters.items():
                filters.append(f'labels.{key}="{value}"')

        if self.text_search:
            filters.append(
                f'textPayload:"{self.text_search}" OR jsonPayload.message:"{self.text_search}"'
            )

        return " AND ".join(filters) if filters else ""


@dataclass
class StructuredLogPayload:
    message: str
    severity: str = "INFO"
    component: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        payload = {"message": self.message, "severity": self.severity}

        if self.component:
            payload["component"] = self.component
        if self.user_id:
            payload["user_id"] = self.user_id
        if self.request_id:
            payload["request_id"] = self.request_id
        if self.additional_fields:
            payload.update(self.additional_fields)

        return payload
