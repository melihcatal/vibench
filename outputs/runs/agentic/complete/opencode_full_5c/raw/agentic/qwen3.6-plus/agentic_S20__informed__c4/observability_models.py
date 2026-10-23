from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class LogEventRequest:
    message: str
    status: str = "info"
    service: Optional[str] = None
    hostname: Optional[str] = None
    ddsource: str = "python"
    ddtags: Optional[str] = None
    timestamp: Optional[str] = None
    correlation_id: Optional[str] = None
    span_id: Optional[str] = None
    trace_id: Optional[str] = None
    custom_attributes: dict = field(default_factory=dict)

    def to_payload(self):
        payload = {
            "message": self.message,
            "ddsource": self.ddsource,
            "hostname": self.hostname or "",
            "status": self.status,
            "timestamp": self.timestamp or datetime.now(timezone.utc).isoformat(),
        }
        if self.service:
            payload["service"] = self.service
        if self.ddtags:
            payload["ddtags"] = self.ddtags
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.span_id:
            payload["span_id"] = self.span_id
        if self.trace_id:
            payload["trace_id"] = self.trace_id
        payload.update(self.custom_attributes)
        return payload


@dataclass
class LogQueryRequest:
    query: str = "*"
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    limit: int = 100
    sort: str = "-timestamp"

    def to_body(self):
        return {
            "filter": {
                "query": self.query,
                "from": self.time_from,
                "to": self.time_to,
            },
            "page": {
                "limit": self.limit,
            },
            "sort": self.sort,
        }


@dataclass
class NormalizedLogEntry:
    timestamp: Optional[str] = None
    message: str = ""
    status: str = "unknown"
    service: str = ""
    hostname: str = ""
    tags: list = field(default_factory=list)
    correlation_id: Optional[str] = None
    raw_attributes: dict = field(default_factory=dict)

    @classmethod
    def from_datadog_event(cls, event_data):
        attributes = event_data.get("attributes", {})
        tags = attributes.get("tags", [])
        return cls(
            timestamp=attributes.get("timestamp"),
            message=attributes.get("message", ""),
            status=attributes.get("status", "unknown"),
            service=attributes.get("service", ""),
            hostname=attributes.get("hostname", ""),
            tags=tags if isinstance(tags, list) else [],
            correlation_id=attributes.get("correlation_id"),
            raw_attributes=attributes,
        )

    def to_dict(self):
        return asdict(self)


@dataclass
class QueryResponse:
    data: list = field(default_factory=list)
    paging: dict = field(default_factory=dict)
    status: Optional[str] = None

    @classmethod
    def from_datadog_response(cls, response_json):
        return cls(
            data=response_json.get("data", []),
            paging=response_json.get("page", {}),
            status=response_json.get("status"),
        )

    def normalized_entries(self):
        return [NormalizedLogEntry.from_datadog_event(evt) for evt in self.data]
