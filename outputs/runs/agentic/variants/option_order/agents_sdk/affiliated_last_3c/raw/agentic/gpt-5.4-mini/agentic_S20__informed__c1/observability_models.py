from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_timestamp(value: Optional[str] = None) -> str:
    return value or utc_now_iso()


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(fields or {})


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    timestamp: str = field(default_factory=utc_now_iso)
    fields: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity.upper(),
            "timestamp": normalize_timestamp(self.timestamp),
            "fields": normalize_fields(self.fields),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        return payload


@dataclass
class LogQuery:
    severity: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    field_filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 50

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "severity": self.severity.upper() if self.severity else None,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "field_filters": normalize_fields(self.field_filters),
            "limit": self.limit,
        }
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class LogQueryResult:
    items: List[Dict[str, Any]]
    count: int
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_items(cls, items: Iterable[Dict[str, Any]], raw: Optional[Dict[str, Any]] = None) -> "LogQueryResult":
        items_list = list(items)
        return cls(items=items_list, count=len(items_list), raw=raw)


@dataclass
class IncidentSummary:
    title: str
    severity: str
    summary: str
    evidence: List[Dict[str, Any]]
    generated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
