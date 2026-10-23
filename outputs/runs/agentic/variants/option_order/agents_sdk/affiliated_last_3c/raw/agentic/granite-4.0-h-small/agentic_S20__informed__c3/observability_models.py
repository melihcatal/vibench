from typing import TypedDict, List, Any

class LogEvent(TypedDict):
    timestamp: int
    level: str
    service: str
    message: str
    correlationId: str | None

class LogQueryResponse(TypedDict):
    events: List[LogEvent]
    nextToken: Any | None

class LogIngestResponse(TypedDict):
    """Dummy response shape for CloudWatch put_log_events."""
    ResponseMetadata: dict

class LogSearchParams(TypedDict):
    startTime: int
    endTime: int
    filterPattern: str
