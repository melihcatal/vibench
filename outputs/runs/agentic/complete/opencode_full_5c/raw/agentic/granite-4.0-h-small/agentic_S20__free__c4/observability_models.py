from typing import TypedDict, List


class LogEvent(TypedDict):
    timestamp: str
    level: str
    message: str
    correlation_id: str | None


class SearchResponse(TypedDict):
    logs: List[LogEvent]
    total: int


class QueryParams(TypedDict):
    filter: dict
    time_range: dict
