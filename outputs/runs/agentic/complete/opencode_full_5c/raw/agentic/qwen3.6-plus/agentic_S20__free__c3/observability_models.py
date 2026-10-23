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
    level: str = LogLevel.INFO.value
    service: str = ""
    source: str = ""
    hostname: str = ""
    tags: list[str] = field(default_factory=list)
    correlation_id: str = ""
    trace_id: str = ""
    span_id: str = ""
    timestamp: Optional[str] = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "message": self.message,
            "ddtags": ",".join(self.tags) if self.tags else "",
            "hostname": self.hostname,
            "service": self.service,
            "source": self.source,
        }
        if self.level:
            payload["status"] = self.level
        if self.correlation_id:
            payload["dd.trace_id"] = self.correlation_id
        if self.trace_id:
            payload["dd.trace_id"] = self.trace_id
        if self.span_id:
            payload["dd.span_id"] = self.span_id
        if self.timestamp:
            payload["datehappened"] = int(
                datetime.fromisoformat(self.timestamp).timestamp()
            )
        for k, v in self.attributes.items():
            payload[k] = v
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LogEvent":
        timestamp = None
        if "datehappened" in data:
            timestamp = datetime.fromtimestamp(
                data["datehappened"], tz=timezone.utc
            ).isoformat()
        elif "@timestamp" in data:
            timestamp = data["@timestamp"]
        tags = []
        if "ddtags" in data and data["ddtags"]:
            tags = [t.strip() for t in data["ddtags"].split(",")]
        attributes = {
            k: v
            for k, v in data.items()
            if k
            not in {
                "message",
                "ddtags",
                "hostname",
                "service",
                "source",
                "status",
                "dd.trace_id",
                "dd.span_id",
                "datehappened",
                "@timestamp",
            }
        }
        return cls(
            message=data.get("message", ""),
            level=data.get("status", LogLevel.INFO.value),
            service=data.get("service", ""),
            source=data.get("source", ""),
            hostname=data.get("hostname", ""),
            tags=tags,
            correlation_id=data.get("dd.trace_id", ""),
            trace_id=data.get("dd.trace_id", ""),
            span_id=data.get("dd.span_id", ""),
            timestamp=timestamp,
            attributes=attributes,
        )


@dataclass
class LogQuery:
    query: str = ""
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    index: str = "main"
    limit: int = 100
    sort: str = "timestamp"
    filter_query: Optional[str] = None

    def to_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"filter[query]": self.query}
        if self.from_time:
            params["filter[from]"] = self.from_time
        if self.to_time:
            params["filter[to]"] = self.to_time
        if self.index:
            params["filter[indexes]"] = self.index
        params["page[limit]"] = self.limit
        params["sort"] = self.sort
        if self.filter_query:
            params["filter[query]"] = self.filter_query
        return params


@dataclass
class LogEntry:
    id: str = ""
    message: str = ""
    level: str = ""
    service: str = ""
    source: str = ""
    hostname: str = ""
    timestamp: str = ""
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""

    @classmethod
    def from_datadog_response(cls, data: dict[str, Any]) -> "LogEntry":
        attrs = data.get("attributes", {})
        tags = attrs.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        return cls(
            id=data.get("id", ""),
            message=attrs.get("message", ""),
            level=attrs.get("status", ""),
            service=attrs.get("service", ""),
            source=attrs.get("source", ""),
            hostname=attrs.get("hostname", ""),
            timestamp=attrs.get("timestamp", ""),
            tags=tags,
            attributes=attrs,
            correlation_id=attrs.get("dd.trace_id", ""),
        )


@dataclass
class LogQueryResponse:
    entries: list[LogEntry] = field(default_factory=list)
    next_page_token: Optional[str] = None
    total_count: int = 0
    status: str = "success"

    @classmethod
    def from_datadog_response(cls, data: dict[str, Any]) -> "LogQueryResponse":
        entries = []
        for log_data in data.get("data", []):
            entries.append(LogEntry.from_datadog_response(log_data))
        meta = data.get("meta", {})
        page = meta.get("page", {})
        return cls(
            entries=entries,
            next_page_token=page.get("after"),
            total_count=meta.get("status", {}).get("resultsCount", len(entries)),
            status="success",
        )


@dataclass
class LogWriteResponse:
    success: bool = True
    event_id: str = ""
    message: str = ""
    status_code: int = 202


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def minutes_ago_iso(minutes: int) -> str:
    from datetime import timedelta

    dt = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return dt.isoformat()


DATADOG_API_HOST = os.environ.get("DD_SITE", "api.datadoghq.com")
DATADOG_API_BASE = f"https://{DATADOG_API_HOST}"
DATADOG_LOGS_INTAKE_URL = f"https://http-intake.logs.{DATADOG_API_HOST}"
DATADOG_API_KEY = os.environ.get("DD_API_KEY", "")
DATADOG_APP_KEY = os.environ.get("DD_APP_KEY", "")
