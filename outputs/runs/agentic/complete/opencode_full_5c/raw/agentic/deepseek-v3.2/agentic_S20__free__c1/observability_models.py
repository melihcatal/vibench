from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime
import json


@dataclass
class LogEvent:
    """Represents a structured log event."""

    timestamp: int
    message: str
    level: str = "INFO"
    correlation_id: Optional[str] = None
    service: Optional[str] = None
    component: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if self.metadata:
            result.update(self.metadata)
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEvent":
        """Create LogEvent from dictionary."""
        # Extract metadata fields
        metadata = {}
        core_fields = {
            "timestamp",
            "message",
            "level",
            "correlation_id",
            "service",
            "component",
        }

        for key in list(data.keys()):
            if key not in core_fields:
                metadata[key] = data.pop(key)

        if metadata:
            data["metadata"] = metadata

        return cls(**data)


@dataclass
class LogQuery:
    """Represents a log query with filters."""

    log_group: str
    start_time: int
    end_time: int
    query_string: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    limit: int = 100

    def to_cloudwatch_query(self) -> str:
        """Convert to CloudWatch Logs Insights query."""
        query_parts = ["fields @timestamp, @message, @logStream, @log"]

        if self.query_string:
            query_parts.append(f"| filter {self.query_string}")
        elif self.field_filters:
            filter_conditions = []
            for field, value in self.field_filters.items():
                if isinstance(value, str):
                    filter_conditions.append(f'@message like /"{field}":.*"{value}"/')
                else:
                    filter_conditions.append(f'@message like /"{field}":{value}/')

            if filter_conditions:
                query_parts.append(f"| filter {' and '.join(filter_conditions)}")

        query_parts.append("| sort @timestamp desc")
        query_parts.append(f"| limit {self.limit}")

        return "\n".join(query_parts)


@dataclass
class QueryResult:
    """Represents the result of a log query."""

    success: bool
    results: List[Dict[str, Any]]
    query_id: Optional[str] = None
    error: Optional[str] = None
    result_count: int = 0

    def __post_init__(self):
        if self.results is None:
            self.results = []
        self.result_count = len(self.results)


@dataclass
class IncidentSummary:
    """Summary of error logs for incident review."""

    incident_id: str
    start_time: int
    end_time: int
    error_count: int
    unique_errors: List[str]
    affected_services: List[str]
    severity_distribution: Dict[str, int]
    sample_logs: List[Dict[str, Any]]
    summary_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SafetyCheckResult:
    """Result of log message safety check."""

    log_id: str
    message: str
    is_safe: bool
    unsafe_categories: List[str]
    confidence: float
    provider: str = "openai"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class TranslationResult:
    """Result of log message translation."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "google"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class EmbeddingResult:
    """Result of log message embedding."""

    log_id: str
    message: str
    embedding: List[float]
    model: str
    provider: str = "huggingface"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def parse_timestamp(timestamp: Any) -> int:
    """Parse timestamp to milliseconds since epoch."""
    if isinstance(timestamp, int):
        return timestamp
    elif isinstance(timestamp, str):
        try:
            # Try to parse ISO format
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except:
            # Try to parse as milliseconds
            try:
                return int(timestamp)
            except:
                raise ValueError(f"Cannot parse timestamp: {timestamp}")
    elif isinstance(timestamp, datetime):
        return int(timestamp.timestamp() * 1000)
    else:
        raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")


def extract_correlation_id(log_data: Dict[str, Any]) -> Optional[str]:
    """Extract correlation ID from log data."""
    # Check common correlation ID field names
    correlation_fields = [
        "correlation_id",
        "correlationId",
        "request_id",
        "requestId",
        "trace_id",
        "traceId",
    ]

    for field in correlation_fields:
        if field in log_data:
            return str(log_data[field])

    # Check in metadata
    if "metadata" in log_data and isinstance(log_data["metadata"], dict):
        for field in correlation_fields:
            if field in log_data["metadata"]:
                return str(log_data["metadata"][field])

    return None
