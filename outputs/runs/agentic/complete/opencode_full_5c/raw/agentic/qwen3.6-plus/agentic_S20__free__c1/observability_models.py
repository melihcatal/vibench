import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any


@dataclass
class LogEvent:
    message: str
    level: str = "info"
    service: str = "default-service"
    hostname: Optional[str] = None
    ddsource: str = "python-observability-client"
    ddtags: Optional[str] = None
    correlation_id: Optional[str] = None
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_datadog_payload(self) -> dict:
        payload = {
            "message": self.message,
            "ddsource": self.ddsource,
            "service": self.service,
            "status": self.level.lower(),
            "timestamp": self.timestamp,
        }
        if self.hostname:
            payload["hostname"] = self.hostname
        if self.ddtags:
            payload["ddtags"] = self.ddtags
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        for key, value in self.custom_attributes.items():
            payload[key] = value
        return payload


@dataclass
class LogQueryRequest:
    query: str
    time_from: str
    time_to: str
    limit: int = 50
    sort: str = "timestamp"
    indices: Optional[List[str]] = None

    def to_datadog_payload(self) -> dict:
        payload = {
            "filter": {
                "query": self.query,
                "from": self.time_from,
                "to": self.time_to,
            },
            "options": {
                "limit": self.limit,
                "sort": self.sort,
            },
        }
        if self.indices:
            payload["filter"]["indices"] = self.indices
        return payload


@dataclass
class LogEntry:
    id: str
    message: str
    status: str
    timestamp: str
    service: str = ""
    hostname: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    raw_event: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQueryResponse:
    entries: List[LogEntry]
    total_count: int = 0
    next_page_token: Optional[str] = None


def normalize_datadog_log_event(raw_event: dict) -> LogEntry:
    attributes = raw_event.get("attributes", {})
    entry = LogEntry(
        id=raw_event.get("id", attributes.get("id", "")),
        message=attributes.get("message", raw_event.get("message", "")),
        status=attributes.get("status", raw_event.get("status", "unknown")),
        timestamp=attributes.get("timestamp", raw_event.get("timestamp", "")),
        service=attributes.get("service", raw_event.get("service", "")),
        hostname=attributes.get("hostname", raw_event.get("hostname", "")),
        attributes=attributes,
        raw_event=raw_event,
    )
    return entry


def normalize_datadog_query_response(raw_response: dict) -> LogQueryResponse:
    data = raw_response.get("data", [])
    meta = raw_response.get("meta", {})
    page = meta.get("page", {})
    entries = [normalize_datadog_log_event(event) for event in data]
    return LogQueryResponse(
        entries=entries,
        total_count=page.get("total", len(entries)),
        next_page_token=page.get("after"),
    )


def serialize_log_event(event: LogEvent) -> str:
    return json.dumps(event.to_datadog_payload())


def serialize_query_request(request: LogQueryRequest) -> str:
    return json.dumps(request.to_datadog_payload())
