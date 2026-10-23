import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional
from enum import Enum


class LogSeverity(str, Enum):
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
    timestamp: str
    message: str
    severity: str
    service: str
    source: str = ""
    hostname: str = ""
    correlation_id: str = ""
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = data.pop("severity")
        if self.correlation_id:
            data["ddtags"] = f"correlation_id:{self.correlation_id}"
            if self.tags:
                data["ddtags"] += "," + ",".join(self.tags)
        elif self.tags:
            data["ddtags"] = ",".join(self.tags)
        return data

    @classmethod
    def now(cls, **kwargs) -> "LogEvent":
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )


@dataclass
class LogQueryRequest:
    query: str
    time_from: str
    time_to: str
    limit: int = 100
    sort: str = "timestamp"
    filter_indexes: list[str] = field(default_factory=list)

    def to_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "filter[query]": self.query,
            "filter[from]": self.time_from,
            "filter[to]": self.time_to,
            "page[limit]": self.limit,
            "sort": self.sort,
        }
        if self.filter_indexes:
            params["filter[indexes]"] = ",".join(self.filter_indexes)
        return params


@dataclass
class LogEntry:
    id: str
    timestamp: str
    message: str
    severity: str
    service: str
    source: str = ""
    hostname: str = ""
    correlation_id: str = ""
    raw_attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_datadog_response(cls, entry: dict[str, Any]) -> "LogEntry":
        attrs = entry.get("attributes", {})
        return cls(
            id=entry.get("id", ""),
            timestamp=attrs.get("timestamp", ""),
            message=attrs.get("message", ""),
            severity=attrs.get("status", "unknown"),
            service=attrs.get("service", ""),
            source=attrs.get("source", ""),
            hostname=attrs.get("hostname", ""),
            correlation_id=attrs.get("correlation_id", ""),
            raw_attributes=attrs,
        )


@dataclass
class LogQueryResponse:
    entries: list[LogEntry]
    total: int = 0
    next_page_token: Optional[str] = None

    @classmethod
    def from_datadog_response(cls, response: dict[str, Any]) -> "LogQueryResponse":
        data = response.get("data", [])
        meta = response.get("meta", {})
        return cls(
            entries=[LogEntry.from_datadog_response(e) for e in data],
            total=meta.get("page", {}).get("total", len(data)),
            next_page_token=meta.get("page", {}).get("after"),
        )


@dataclass
class IngestionResponse:
    success: bool
    status_code: int
    message: str = ""
    event_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_datadog_response(
        cls, status_code: int, body: dict[str, Any]
    ) -> "IngestionResponse":
        return cls(
            success=200 <= status_code < 300,
            status_code=status_code,
            message=body.get("error", ""),
            event_ids=body.get("event_ids", []),
        )
