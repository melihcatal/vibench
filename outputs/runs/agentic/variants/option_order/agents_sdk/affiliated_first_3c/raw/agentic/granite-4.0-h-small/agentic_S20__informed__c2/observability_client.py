import os
from typing import Protocol, TypedDict

# Provider-agnostic interface for log ingestion and query

class LogPayload(TypedDict):
    message: str
    timestamp: str               # ISO 8601 string
    level: str                    # e.g., DEBUG, INFO, WARNING, ERROR
    correlation_id: str | None
    source: str | None = None
    tags: list[str] | None = None


class QuerySpec(TypedDict):
    query: str
    start_time: str
    end_time: str | None
    limit: int | None
    tags: list[str] | None


class ObservabilityClient(Protocol):
    """Protocol representing a managed logging service client."""
    def ingest(self, payload: LogPayload) -> dict:
        ...  # Should return provider-specific response
    
    def query(self, spec: QuerySpec) -> dict:
        ...  # Should return provider-specific response
