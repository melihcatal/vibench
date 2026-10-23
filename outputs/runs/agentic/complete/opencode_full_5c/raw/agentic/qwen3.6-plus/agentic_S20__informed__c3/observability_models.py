from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class LogEvent:
    message: str
    level: str
    service: str
    source: str
    correlation_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    extra_attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        ts = self.timestamp or datetime.now(timezone.utc)
        ddtags = [
            f"service:{self.service}",
            f"source:{self.source}",
            f"level:{self.level}",
        ]
        if self.correlation_id:
            ddtags.append(f"correlation_id:{self.correlation_id}")
        payload = {
            "ddsource": self.source,
            "ddtags": ",".join(ddtags),
            "message": self.message,
            "service": self.service,
            "status": self.level.upper(),
            "timestamp": int(ts.timestamp() * 1000),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.extra_attributes:
            payload.update(self.extra_attributes)
        return payload


@dataclass
class LogQuery:
    query: str
    start_time: datetime
    end_time: datetime
    limit: int = 50
    sort: str = "timestamp"

    def to_body(self) -> dict:
        return {
            "filter": {
                "query": self.query,
                "from": self.start_time.isoformat(),
                "to": self.end_time.isoformat(),
            },
            "page": {
                "limit": self.limit,
            },
            "sort": self.sort,
        }


@dataclass
class LogEntry:
    id: str
    timestamp: str
    message: str
    status: str
    service: str
    tags: list = field(default_factory=list)
    attributes: dict = field(default_factory=dict)

    @classmethod
    def from_datadog_event(cls, event: dict) -> "LogEntry":
        attrs = event.get("attributes", {})
        return cls(
            id=event.get("id", ""),
            timestamp=attrs.get("timestamp", ""),
            message=attrs.get("message", ""),
            status=attrs.get("status", ""),
            service=attrs.get("service", ""),
            tags=attrs.get("tags", []),
            attributes=attrs,
        )


def normalize_log_entries(raw_events: list[dict]) -> list[LogEntry]:
    return [LogEntry.from_datadog_event(e) for e in raw_events]


def format_log_for_display(entry: LogEntry) -> str:
    return f"[{entry.timestamp}] {entry.status} service={entry.service} {entry.message}"
