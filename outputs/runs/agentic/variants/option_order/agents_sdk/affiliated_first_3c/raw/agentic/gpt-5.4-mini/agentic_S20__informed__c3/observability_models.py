from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_severity(severity: str) -> str:
    return severity.strip().upper()


def normalize_log_record(record: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(record)
    if "severity" in normalized and isinstance(normalized["severity"], str):
        normalized["severity"] = normalize_severity(normalized["severity"])
    if "timestamp" not in normalized:
        normalized["timestamp"] = utc_now_iso()
    return normalized


@dataclass
class LogEvent:
    timestamp: str
    severity: str
    message: str
    source: str = "application"
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "timestamp": self.timestamp,
            "severity": normalize_severity(self.severity),
            "message": self.message,
            "source": self.source,
            "attributes": dict(self.attributes),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        return normalize_log_record(payload)


@dataclass
class QueryFilter:
    severity: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    field_name: Optional[str] = None
    field_value: Optional[str] = None
    limit: int = 50

    def to_query_params(self) -> Dict[str, Any]:
        params: Dict[str, Any] = {"limit": self.limit}
        if self.severity:
            params["severity"] = normalize_severity(self.severity)
        if self.start_time:
            params["start_time"] = self.start_time
        if self.end_time:
            params["end_time"] = self.end_time
        if self.field_name:
            params["field_name"] = self.field_name
        if self.field_value:
            params["field_value"] = self.field_value
        return params


@dataclass
class QueryResponse:
    records: List[Dict[str, Any]]
    raw: Optional[Any] = None


@dataclass
class IncidentSummary:
    title: str
    severity: str
    findings: List[str]
    affected_correlation_ids: List[str] = field(default_factory=list)
    suggested_next_steps: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "severity": normalize_severity(self.severity),
            "findings": list(self.findings),
            "affected_correlation_ids": list(self.affected_correlation_ids),
            "suggested_next_steps": list(self.suggested_next_steps),
        }
