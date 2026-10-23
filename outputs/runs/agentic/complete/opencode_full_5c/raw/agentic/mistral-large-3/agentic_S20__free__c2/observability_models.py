from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    """
    A normalized log entry model for ingestion and query responses.
    """

    message: str
    level: str = Field(..., alias="status")
    timestamp: str
    service: str
    correlation_id: Optional[str] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        allow_population_by_field_name = True


class LogQueryRequest(BaseModel):
    """
    A request model for querying logs.
    """

    query: str
    start_time: str
    end_time: str
    limit: int = 100


class LogQueryResponse(BaseModel):
    """
    A response model for log query results.
    """

    logs: List[LogEntry]
    total: int


def normalize_log_entry(raw_log: Dict[str, Any]) -> LogEntry:
    """
    Normalizes a raw log entry into a structured LogEntry.

    Args:
        raw_log: A dictionary representing a raw log entry.

    Returns:
        A normalized LogEntry instance.
    """
    return LogEntry(**raw_log)


def normalize_query_response(raw_response: Dict[str, Any]) -> LogQueryResponse:
    """
    Normalizes a raw query response into a structured LogQueryResponse.

    Args:
        raw_response: A dictionary representing a raw query response.

    Returns:
        A normalized LogQueryResponse instance.
    """
    logs = [normalize_log_entry(log) for log in raw_response.get("logs", [])]
    return LogQueryResponse(logs=logs, total=len(logs))
