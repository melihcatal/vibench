from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LogWriteRequest:
    service: str
    message: str
    level: str = "info"
    hostname: str = ""
    correlation_id: Optional[str] = None
    attributes: dict = field(default_factory=dict)
    timestamp_ms: Optional[int] = None


@dataclass
class LogWriteResponse:
    success: bool
    event_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class LogQueryRequest:
    filters: list = field(default_factory=list)
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    limit: int = 50
    sort: str = "timestamp"


@dataclass
class LogEntry:
    id: str = ""
    timestamp: str = ""
    status: str = ""
    service: str = ""
    message: str = ""
    host: str = ""
    correlation_id: Optional[str] = None
    attributes: dict = field(default_factory=dict)


@dataclass
class LogQueryResponse:
    entries: list = field(default_factory=list)
    next_page_token: Optional[str] = None
    error: Optional[str] = None


def normalize_log_write_response(
    status_code: int, response_body: dict
) -> LogWriteResponse:
    if status_code in (200, 202, 204):
        return LogWriteResponse(
            success=True,
            event_id=response_body.get("id", response_body.get("event_id", "")),
        )
    return LogWriteResponse(
        success=False,
        error=response_body.get("error", {}).get("message", f"HTTP {status_code}"),
    )


def normalize_log_query_response(response_body: dict) -> LogQueryResponse:
    raw_data = response_body.get("data", [])
    entries = []
    for raw_entry in raw_data:
        attrs = raw_entry.get("attributes", {})
        entry = LogEntry(
            id=raw_entry.get("id", ""),
            timestamp=attrs.get("timestamp", ""),
            status=attrs.get("status", attrs.get("level", "")),
            service=attrs.get("service", ""),
            message=attrs.get("message", ""),
            host=attrs.get("host", ""),
            correlation_id=attrs.get(
                "correlation_id", attrs.get("request_id", attrs.get("trace_id"))
            ),
            attributes=attrs,
        )
        entries.append(entry)
    next_page = response_body.get("meta", {}).get("page", {}).get("after")
    return LogQueryResponse(entries=entries, next_page_token=next_page)
