from typing import TypedDict, Literal


class LogEvent(TypedDict):
    timestamp: str
    service: str
    message: str
    severity: Literal["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
    request_id: str | None
    environment: str


class QueryExpression(TypedDict):
    text: str
    field: str | None


class QueryFilter(TypedDict):
    severity: str | None
    timestamp_range: dict | None
    # Add any provider‑specific filters as additional keys


class QueryResult(TypedDict):
    events: list[LogEvent]
    total: int


class CorrelationContext(TypedDict):
    request_id: str
    user_id: str | None
    operation: str | None
