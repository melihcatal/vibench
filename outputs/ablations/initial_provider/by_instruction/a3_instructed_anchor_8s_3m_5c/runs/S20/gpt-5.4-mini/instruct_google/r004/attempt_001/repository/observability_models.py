from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    message: str
    severity: str
    labels: Dict[str, str]
    correlation_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    extra: Optional[Dict[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.extra is None:
            data.pop("extra")
        return data


@dataclass
class QueryResult:
    entries: List[Dict[str, Any]]


@dataclass
class IncidentSummary:
    title: str
    severity_counts: Dict[str, int]
    sample_messages: List[str]


def extract_message(entry: Dict[str, Any]) -> str:
    for key in ("message", "textPayload", "summary"):
        value = entry.get(key)
        if value:
            return str(value)
    return ""


def extract_severity(entry: Dict[str, Any]) -> str:
    return str(entry.get("severity") or entry.get("logSeverity") or "DEFAULT")
