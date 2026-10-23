from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_fields(fields: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    if not fields:
        return {}
    normalized: Dict[str, Any] = {}
    for key, value in fields.items():
        if value is None:
            continue
        normalized[str(key)] = value
    return normalized


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    service: str = "app"
    correlation_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": self.message,
            "severity": self.severity,
            "service": self.service,
            "timestamp": self.timestamp,
            **normalize_fields(self.fields),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        return payload


@dataclass
class QueryRequest:
    query: str
    start_time: str
    end_time: str
    limit: int = 100


@dataclass
class QueryResponse:
    entries: List[Dict[str, Any]]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IngestResponse:
    accepted: bool
    raw: Dict[str, Any] = field(default_factory=dict)
