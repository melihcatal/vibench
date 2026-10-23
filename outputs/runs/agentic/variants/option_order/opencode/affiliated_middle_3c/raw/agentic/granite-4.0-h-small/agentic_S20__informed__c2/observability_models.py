from typing import TypedDict, List, Optional


class LogMessage(TypedDict):
    timestamp: int  # epoch milliseconds
    level: str  # e.g. INFO, ERROR
    message: str

    # Optional correlation identifier used for tracing
    correlation_id: Optional[str]

    # Optional user or request attributes
    user_id: Optional[int]
    request_id: Optional[str]

    # Any additional structured fields
    extra: Optional[dict]


class LogQueryParams(TypedDict):
    schema: str  # e.g. AzureDiagnostics, syslog
    filter: str  # raw query filter string
    start: Optional[str]  # ISO8601 timestamp
    end: Optional[str]  # ISO8601 timestamp
    limit: Optional[int]

    # Optional fields for response format control
    format: Optional[str]  # json, csv
