from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class LogEvent:
    message: str
    severity: str
    timestamp: str
    service: str
    source: str
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQuery:
    severity: Optional[str]
    start_time: str
    end_time: str
    source: str
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 50


@dataclass
class LogResult:
    results: List[Dict[str, Any]]
    count: int
    query: LogQuery


@dataclass
class ParsedLogResponse:
    status: str
    request_id: str
    accepted: bool
    results: List[Dict[str, Any]]


def normalize_event(event: LogEvent) -> Dict[str, Any]:
    payload = {
        "message": event.message,
        "severity": event.severity,
        "timestamp": event.timestamp,
        "service": event.service,
        "source": event.source,
        "insert_id": str(uuid.uuid4()),
    }
    if event.correlation_id:
        payload["correlation_id"] = event.correlation_id
    payload.update(event.fields)
    return payload


def build_structured_log_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload


def build_batch_log_payload(payloads: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"entries": payloads}


def normalize_query_result(result: LogResult) -> Dict[str, Any]:
    return {"count": result.count, "results": result.results, "query": {"severity": result.query.severity, "start_time": result.query.start_time, "end_time": result.query.end_time, "source": result.query.source, "field_filters": result.query.field_filters, "limit": result.query.limit}}
