from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    timestamp: str
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQueryRequest:
    start_time: str
    end_time: str
    severity: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 50


@dataclass
class LogQueryResult:
    entries: List[Dict[str, Any]]
    raw_response: Dict[str, Any]


def normalize_log_event(event: LogEvent) -> Dict[str, Any]:
    payload = {
        "timestamp": event.timestamp,
        "severity": event.severity,
        "message": event.message,
        "service": event.service,
        **event.fields,
    }
    if event.correlation_id is not None:
        payload["correlation_id"] = event.correlation_id
    return payload


def normalize_query_filters(request: LogQueryRequest) -> Dict[str, Any]:
    filters = {
        "start_time": request.start_time,
        "end_time": request.end_time,
        "limit": request.limit,
    }
    if request.severity:
        filters["severity"] = request.severity
    filters.update(request.field_filters)
    return filters
