from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LogEvent:
    message: str
    level: str = "info"
    service: Optional[str] = None
    env: Optional[str] = None
    ddsource: str = "python"
    hostname: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuerySpec:
    query: str
    start: datetime
    end: datetime
    limit: int = 50

    def to_datadog_params(self) -> Dict[str, Any]:
        return {
            "filter[query]": self.query,
            "filter[from]": self.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "filter[to]": self.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "page[limit]": self.limit,
        }


@dataclass
class LogResponse:
    raw: Dict[str, Any]

    def messages(self) -> List[str]:
        items = self.raw.get("data", [])
        out: List[str] = []
        for item in items:
            attrs = item.get("attributes", {}) if isinstance(item, dict) else {}
            out.append(str(attrs.get("message", "")))
        return out


def normalize_event(event: LogEvent, default_service: str, default_env: str) -> Dict[str, Any]:
    payload = {
        "message": event.message,
        "status": event.level.lower(),
        "ddsource": event.ddsource,
        "service": event.service or default_service,
        "env": event.env or default_env,
    }
    if event.hostname:
        payload["hostname"] = event.hostname
    if event.tags:
        payload["tags"] = [f"{k}:{v}" for k, v in event.tags.items()]
    payload.update(event.extra)
    return payload


def build_correlation_query(correlation_id: str, level: Optional[str] = None) -> str:
    parts = [f'correlation_id:{correlation_id}']
    if level:
        parts.append(f'status:{level.lower()}')
    return " ".join(parts)


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
