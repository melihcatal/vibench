from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class LogEntryPayload:
    data: Dict[str, Any]
    severity: str = "INFO"
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class LogQueryRequest:
    severity: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    fields: Dict[str, str] = field(default_factory=dict)
    limit: int = 50


@dataclass
class LogQueryResponse:
    entries: List[Dict[str, Any]]


@dataclass
class IncidentSummary:
    title: str
    details: str
    affected_services: List[str] = field(default_factory=list)
    error_count: int = 0


def normalize_labels(labels: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in labels.items()}


def entry_to_dict(entry: Any) -> Dict[str, Any]:
    payload = getattr(entry, "payload", {})
    if hasattr(payload, "items"):
        payload = dict(payload)
    return {
        "log_name": getattr(entry, "log_name", None),
        "severity": getattr(entry, "severity", None),
        "timestamp": getattr(entry, "timestamp", None).isoformat() if getattr(entry, "timestamp", None) else None,
        "payload": payload,
    }
