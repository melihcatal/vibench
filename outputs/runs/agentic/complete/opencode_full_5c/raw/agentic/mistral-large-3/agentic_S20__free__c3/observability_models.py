from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class StructuredLogEvent(BaseModel):
    """Model for structured log events."""

    message: str
    severity: str
    service_name: str
    timestamp: Optional[datetime] = None
    tags: Dict[str, str] = {}
    custom_fields: Dict[str, Any] = {}


class CorrelatedLogEvent(BaseModel):
    """Model for correlated log events with a shared identifier."""

    message: str
    severity: str
    correlation_id: str
    service_name: str
    log_group: str
    log_stream: str
    timestamp: datetime
    tags: Dict[str, str] = {}
    custom_fields: Dict[str, Any] = {}


class LogQueryFilter(BaseModel):
    """Filter for querying logs by severity and time range."""

    severities: List[str]
    time_range_seconds: int
    limit: int = 100


class LogFetchFilter(BaseModel):
    """Filter for fetching logs by field values and time range."""

    field_filters: Dict[str, str]
    time_range_seconds: int
    limit: int = 100
    log_table: str = "AppEvents"
