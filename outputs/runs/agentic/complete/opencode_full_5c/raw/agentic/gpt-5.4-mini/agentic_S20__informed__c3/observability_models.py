from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_iso(dt: Optional[datetime] = None) -> str:
    dt = dt or datetime.now(timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


@dataclass
class LogEvent:
    message: str
    level: str
    service: str
    timestamp: str
    logger: str = "app"
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

    def to_datadog(self) -> Dict[str, Any]:
        data = {
            "message": normalize_text(self.message),
            "level": self.level,
            "service": self.service,
            "timestamp": self.timestamp,
            "logger": self.logger,
        }
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        if self.request_id:
            data["request_id"] = self.request_id
        if self.fields:
            data.update(self.fields)
        return data


@dataclass
class QueryWindow:
    start: str
    end: str
    filter_query: str


def build_severity_query(
    severity: str, service: str, extra: Optional[str] = None
) -> str:
    parts = [f"service:{service}", f"level:{severity}"]
    if extra:
        parts.append(extra)
    return " ".join(parts)


def build_field_query(field: str, value: str, service: str) -> str:
    return f"service:{service} {field}:{value}"


def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
