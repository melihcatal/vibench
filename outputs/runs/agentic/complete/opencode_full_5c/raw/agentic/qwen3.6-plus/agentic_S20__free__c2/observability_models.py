from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime, timezone


@dataclass
class LogEvent:
    message: str
    status: str = "info"
    service: str = ""
    source: str = ""
    tags: list[str] = field(default_factory=list)
    correlation_id: str = ""
    timestamp: Optional[datetime] = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_datadog_payload(self) -> dict:
        ts = self.timestamp or datetime.now(timezone.utc)
        payload = {
            "ddsource": self.source or "python",
            "ddtags": ",".join(self.tags) if self.tags else "",
            "hostname": "",
            "message": self.message,
            "service": self.service,
            "status": self.status,
            "timestamp": int(ts.timestamp() * 1000),
        }
        if self.correlation_id:
            payload["dd.trace_id"] = self.correlation_id
            payload["correlation_id"] = self.correlation_id
        if self.attributes:
            payload.update(self.attributes)
        return payload


@dataclass
class LogQueryRequest:
    query: str = ""
    index: str = "main"
    from_ts: Optional[datetime] = None
    to_ts: Optional[datetime] = None
    limit: int = 100
    sort: str = "timestamp"

    def to_params(self) -> dict:
        params: dict[str, Any] = {
            "filter[query]": self.query,
            "filter[indexes]": self.index,
            "page[limit]": self.limit,
            "sort": self.sort,
        }
        if self.from_ts:
            params["filter[from]"] = f"{int(self.from_ts.timestamp())}s"
        if self.to_ts:
            params["filter[to]"] = f"{int(self.to_ts.timestamp())}s"
        return params


@dataclass
class LogEntry:
    id: str
    message: str
    status: str
    timestamp: datetime
    service: str = ""
    source: str = ""
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""


@dataclass
class LogQueryResponse:
    entries: list[LogEntry]
    next_page_token: Optional[str] = None
    total_count: int = 0


@dataclass
class LogWriteResponse:
    success: bool
    event_count: int = 0
    errors: list[str] = field(default_factory=list)


def normalize_datadog_log(raw: dict) -> LogEntry:
    attributes = raw.get("attributes", {})
    tags_raw = attributes.get("tags", [])
    tags = tags_raw if isinstance(tags_raw, list) else []
    ts_str = attributes.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        ts = datetime.now(timezone.utc)
    correlation_id = (
        attributes.get("correlation_id", "") or attributes.get("dd.trace_id", "") or ""
    )
    return LogEntry(
        id=raw.get("id", ""),
        message=attributes.get("message", ""),
        status=attributes.get("status", "info"),
        timestamp=ts,
        service=attributes.get("service", ""),
        source=attributes.get("ddsource", ""),
        tags=tags,
        attributes=attributes,
        correlation_id=correlation_id,
    )
