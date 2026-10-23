from typing import TypedDict, Optional, List, Any


class StructuredLogPayload(TypedDict):
    message: str
    user_id: Optional[str]
    request_id: Optional[str]
    metadata: Optional[dict[str, Any]]


class LogEntry(TypedDict):
    severity: str
    payload: StructuredLogPayload


class QueryResult(TypedDict):
    timestamp: str
    severity: str
    message: str
    payload: dict[str, Any]
