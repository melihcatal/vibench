from typing import TypedDict, List, Dict, Any, Optional
import json


class LogEvent(TypedDict):
    message: str
    service: Optional[str]
    status: Optional[str]
    timestamp: Optional[float]
    host: Optional[str]
    correlation_id: Optional[str]


class QueryLogsResponse(TypedDict):
    data: List[Dict[str, Any]]


def serialize_log_event(event: LogEvent) -> str:
    return json.dumps(event, default=str)


def serialize_logs(logs: List[LogEvent]) -> str:
    return json.dumps(logs, default=str)
