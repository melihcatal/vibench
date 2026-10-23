import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    NOTICE = "notice"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    ALERT = "alert"
    EMERGENCY = "emergency"


@dataclass
class LogEvent:
    message: str
    level: LogLevel = LogLevel.INFO
    service: str = ""
    source: str = ""
    hostname: str = ""
    correlation_id: str = ""
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "message": self.message,
            "ddtags": ",".join(self.tags) if self.tags else "",
            "service": self.service,
            "hostname": self.hostname,
            "status": self.level.value,
        }
        if self.source:
            payload["ddsource"] = self.source
        if self.correlation_id:
            payload["dd.request_id"] = self.correlation_id
        if self.attributes:
            payload.update(self.attributes)
        if self.timestamp:
            payload["timestamp"] = self.timestamp
        return payload


@dataclass
class LogQueryRequest:
    query: str = ""
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    limit: int = 100
    sort: str = "timestamp"

    def to_datadog_query(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "filter": {
                "query": self.query,
                "from": self.time_from or "now-1h",
                "to": self.time_to or "now",
            },
            "page": {"limit": self.limit},
            "sort": self.sort,
        }
        if self.filter_field and self.filter_value:
            existing = body["filter"]["query"]
            extra = f'{self.filter_field}:"{self.filter_value}"'
            body["filter"]["query"] = f"{existing} {extra}" if existing else extra
        return body


@dataclass
class LogEntry:
    id: str = ""
    message: str = ""
    status: str = ""
    service: str = ""
    hostname: str = ""
    timestamp: str = ""
    correlation_id: str = ""
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_datadog_response(cls, event: dict[str, Any]) -> "LogEntry":
        attrs = event.get("attributes", {})
        tags = attrs.get("tags", [])
        return cls(
            id=event.get("id", ""),
            message=attrs.get("message", ""),
            status=attrs.get("status", ""),
            service=attrs.get("service", ""),
            hostname=attrs.get("hostname", ""),
            timestamp=attrs.get("timestamp", ""),
            correlation_id=attrs.get("dd.request_id", ""),
            tags=tags if isinstance(tags, list) else [],
            attributes={
                k: v
                for k, v in attrs.items()
                if k
                not in (
                    "message",
                    "status",
                    "service",
                    "hostname",
                    "timestamp",
                    "tags",
                    "dd.request_id",
                )
            },
        )


@dataclass
class LogQueryResponse:
    entries: list[LogEntry] = field(default_factory=list)
    next_page_token: Optional[str] = None
    total_count: int = 0

    @classmethod
    def from_datadog_response(cls, data: dict[str, Any]) -> "LogQueryResponse":
        entries = [LogEntry.from_datadog_response(e) for e in data.get("data", [])]
        meta = data.get("meta", {})
        page = meta.get("page", {})
        return cls(
            entries=entries,
            next_page_token=page.get("after"),
            total_count=page.get("total", len(entries)),
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def minutes_ago_iso(minutes: int) -> str:
    from datetime import timedelta

    dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
