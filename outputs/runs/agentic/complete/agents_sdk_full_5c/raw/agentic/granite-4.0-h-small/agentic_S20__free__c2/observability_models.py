from typing import TypedDict, List, Any, Dict

class LogEvent(TypedDict):
    timestamp: int | None
    event_type: str
    message: str
    metadata: Dict[str, Any]


class ErrorMessage(TypedDict):
    correlation_id: str
    severity: str
    message: str
    timestamp: int


class FetchFilter(TypedDict):
    field: str
    value: Any


class TimeRange(TypedDict):
    from_: str  # ISO8601 string
    to: str    # ISO8601 string


class LokiQuery(TypedDict):
    query: str
    start: str
    limit: int | None


class LogLevel(TypedDict):
    level: str

class IncidentData(TypedDict):
    incident_id: str
    correlation_ids: List[str]
    error_messages: List[ErrorMessage]
    summary: str