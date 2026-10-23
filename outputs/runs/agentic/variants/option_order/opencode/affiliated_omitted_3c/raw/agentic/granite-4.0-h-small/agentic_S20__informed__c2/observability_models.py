from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class LogEvent(BaseModel):
    timestamp: str = Field(
        ..., description="ISO 8601 UTC timestamp, e.g., 2025-01-01T12:34:56Z"
    )
    message: str = Field(..., description="Log message text")
    level: str = Field(..., description="Log severity, e.g., INFO, ERROR, DEBUG")
    correlation_id: Optional[str] = Field(
        None, description="Shared request/tracking ID"
    )
    # Arbitrary extra fields can be added via `extra=True`


class QueryFilters(BaseModel):
    time_range: Dict[str, str] = Field(
        ..., description="Start and end timestamps in ISO 8601 format"
    )
    severity: Optional[str] = Field(None, description="Log level to filter by")
    field_filter: Optional[Dict[str, Any]] = Field(
        None, description="Additional field=value pairs"
    )

    class Config:
        extra = "allow"


class LogQueryResponse(BaseModel):
    logs: List[Dict[str, Any]] = Field(
        ..., description="List of log events matching the query"
    )
    total: int = Field(..., description="Total matching log count across all pages")


class LogIngestResponse(BaseModel):
    status: str = Field(
        ..., description="Status of the ingestion (e.g., 'ok' or error message)"
    )
    reference_id: Optional[str] = Field(
        None, description="Provider‑generated ID for the batch"
    )
