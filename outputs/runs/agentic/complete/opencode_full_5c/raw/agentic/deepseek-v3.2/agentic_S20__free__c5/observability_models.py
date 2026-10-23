from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class StructuredLogEvent:
    """Model for structured log events."""

    service: str
    level: str
    message: str
    timestamp: str
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "service": self.service,
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp,
            **self.extra_fields,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class CorrelatedLogBatch:
    """Model for a batch of correlated logs."""

    correlation_id: str
    service: str
    logs: List[StructuredLogEvent]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "correlation_id": self.correlation_id,
            "service": self.service,
            "timestamp": self.timestamp,
            "log_count": len(self.logs),
            "logs": [log.to_dict() for log in self.logs],
        }


@dataclass
class LogQuery:
    """Model for log query parameters."""

    service: str
    start_time: str
    end_time: str
    filters: Dict[str, str] = field(default_factory=dict)
    limit: int = 100
    severity: Optional[str] = None

    def to_query_string(self, provider: str) -> str:
        """Convert to provider-specific query string."""
        if provider == "aws":
            filter_parts = []
            if self.severity:
                filter_parts.append(f"@message like /?{self.severity}/")
            for key, value in self.filters.items():
                filter_parts.append(f'{key} = "{value}"')

            filter_clause = " | ".join(filter_parts) if filter_parts else ""
            return f"fields @timestamp, @message | {filter_clause} | sort @timestamp desc | limit {self.limit}"

        elif provider == "azure":
            filter_parts = []
            if self.severity:
                filter_parts.append(f"SeverityLevel >= {self.severity}")
            for key, value in self.filters.items():
                filter_parts.append(f'{key} contains "{value}"')

            filter_clause = (
                "\n| where " + " and ".join(filter_parts) if filter_parts else ""
            )
            return f"""
            AppRequests
            | where TimeGenerated between(datetime({self.start_time}) .. datetime({self.end_time}))
            | where AppRoleName contains "{self.service}"
            {filter_clause}
            | project TimeGenerated, AppRoleName, Message, SeverityLevel
            | order by TimeGenerated desc
            | take {self.limit}
            """

        else:
            return ""


@dataclass
class LogEntry:
    """Model for normalized log entry."""

    timestamp: str
    message: str
    service: str
    level: str = "INFO"
    operation: Optional[str] = None
    client_ip: Optional[str] = None
    success: Optional[bool] = None
    log_stream: Optional[str] = None
    log_group: Optional[str] = None
    correlation_id: Optional[str] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "timestamp": self.timestamp,
            "message": self.message,
            "service": self.service,
            "level": self.level,
        }

        if self.operation:
            result["operation"] = self.operation
        if self.client_ip:
            result["client_ip"] = self.client_ip
        if self.success is not None:
            result["success"] = self.success
        if self.log_stream:
            result["log_stream"] = self.log_stream
        if self.log_group:
            result["log_group"] = self.log_group
        if self.correlation_id:
            result["correlation_id"] = self.correlation_id

        return result


@dataclass
class IncidentSummary:
    """Model for incident summary from error logs."""

    incident_id: str
    service: str
    start_time: str
    end_time: str
    error_count: int
    unique_errors: List[str]
    affected_operations: List[str]
    severity: str
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "incident_id": self.incident_id,
            "service": self.service,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error_count": self.error_count,
            "unique_error_count": len(self.unique_errors),
            "unique_errors": self.unique_errors,
            "affected_operations": self.affected_operations,
            "severity": self.severity,
            "summary": self.summary,
        }


@dataclass
class LogSafetyCheck:
    """Model for log message safety check results."""

    message: str
    is_safe: bool
    unsafe_categories: List[str]
    confidence: float
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message": self.message[:100] + "..."
            if len(self.message) > 100
            else self.message,
            "is_safe": self.is_safe,
            "unsafe_categories": self.unsafe_categories,
            "confidence": self.confidence,
            "provider": self.provider,
        }


@dataclass
class TranslatedLog:
    """Model for translated log message."""

    original_message: str
    translated_message: str
    source_language: str
    target_language: str
    confidence: float
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "original_message": self.original_message[:100] + "..."
            if len(self.original_message) > 100
            else self.original_message,
            "translated_message": self.translated_message[:100] + "..."
            if len(self.translated_message) > 100
            else self.translated_message,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
            "provider": self.provider,
        }


@dataclass
class LogEmbedding:
    """Model for log message embedding."""

    message: str
    embedding: List[float]
    model: str
    dimensions: int
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message": self.message[:100] + "..."
            if len(self.message) > 100
            else self.message,
            "embedding_length": len(self.embedding),
            "embedding_preview": self.embedding[:5] if self.embedding else [],
            "model": self.model,
            "dimensions": self.dimensions,
            "provider": self.provider,
        }
