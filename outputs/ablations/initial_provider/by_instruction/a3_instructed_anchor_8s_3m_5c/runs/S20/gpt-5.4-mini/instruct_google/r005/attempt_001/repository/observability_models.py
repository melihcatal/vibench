from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LogRecord:
    message: str
    severity: str = "INFO"
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogQuery:
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    severity: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    limit: int = 100


def as_iso(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat()


def build_structured_payload(record: LogRecord) -> Dict[str, Any]:
    data = dict(record.payload)
    data["message"] = record.message
    data["severity"] = record.severity
    data["timestamp"] = as_iso(record.timestamp)
    if record.labels:
        data["labels"] = dict(record.labels)
    return data


def normalize_entries(entries: Iterable[Any]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for entry in entries:
        result.append({"payload": getattr(entry, "payload", None), "severity": getattr(entry, "severity", None), "timestamp": getattr(entry, "timestamp", None)})
    return result
