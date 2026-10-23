from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_message(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_severity(value: Any) -> str:
    severity = normalize_message(value).upper()
    return severity if severity else "INFO"


def build_event(
    message: str,
    severity: str = "INFO",
    service: str = "app",
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    event = {
        "timestamp": utc_now_iso(),
        "service": service,
        "severity": normalize_severity(severity),
        "message": normalize_message(message),
    }
    if request_id:
        event["request_id"] = normalize_message(request_id)
    if correlation_id:
        event["correlation_id"] = normalize_message(correlation_id)
    if extra:
        event.update(extra)
    return event


def ensure_list(value: Optional[Iterable[Any]]) -> List[Any]:
    if value is None:
        return []
    return list(value)


@dataclass
class LogQueryRequest:
    start_time: str
    end_time: str
    filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 100


@dataclass
class LogQueryResponse:
    records: List[Dict[str, Any]]
    next_token: Optional[str] = None


@dataclass
class IncidentSummary:
    title: str
    summary: str
    error_count: int
    severity_breakdown: Dict[str, int]
