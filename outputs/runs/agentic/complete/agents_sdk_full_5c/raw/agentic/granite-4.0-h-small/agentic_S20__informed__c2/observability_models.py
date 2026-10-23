from typing import TypedDict, Dict
import datetime

# Request models for log ingestion

class LogEntry(TypedDict):
    timestamp: str  # ISO8601 string
    level: str      # e.g., INFO, ERROR
    message: str    # raw log text
    fields: dict     # optional additional key/value pairs

class CorrelatedLogBatch(TypedDict):
    correlation_id: str             # UUID / request identifier
    logs: list[LogEntry]            # list of individual log entries

# Response models for query operations

class LogRecord(TypedDict):
    __topic__: str | None
    __severity__: str
    __time__: str                    # ISO8601 timestamp
    __source__: str                  # host or container identifier
    content: str                     # JSON string of the logged payload
}
