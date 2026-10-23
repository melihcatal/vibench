from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json
import uuid


@dataclass
class StructuredLogEvent:
    message: str
    severity: str = "INFO"
    service: str = "application"
    environment: str = "production"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_json_message(self) -> str:
        payload = {
            "message": self.message,
            "severity": self.severity.upper(),
            "service": self.service,
            "environment": self.environment,
            "timestamp": self.timestamp.astimezone(timezone.utc).isoformat(),
            "correlation_id": self.correlation_id,
            **self.attributes,
        }
        return json.dumps({k: v for k, v in payload.items() if v is not None}, separators=(",", ":"), default=str)


@dataclass
class LogQueryWindow:
    start_time: datetime
    end_time: datetime
    limit: int = 100

    def validate(self) -> None:
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        if self.limit <= 0:
            raise ValueError("limit must be positive")


@dataclass
class NormalizedLogEntry:
    timestamp: str
    message: str
    fields: Dict[str, Any]


@dataclass
class QueryResult:
    query_id: str
    status: str
    results: List[NormalizedLogEntry]


def ensure_correlation_id(value: Optional[str] = None) -> str:
    return value or str(uuid.uuid4())


def epoch_seconds(dt: datetime) -> int:
    return int(dt.astimezone(timezone.utc).timestamp())


def normalize_cloudwatch_results(rows: Iterable[Iterable[Dict[str, str]]]) -> List[NormalizedLogEntry]:
    entries: List[NormalizedLogEntry] = []
    for row in rows:
        mapped = {item.get("field", ""): item.get("value") for item in row}
        timestamp = mapped.get("@timestamp", "")
        message = mapped.get("@message", "")
        entries.append(NormalizedLogEntry(timestamp=timestamp, message=message, fields=mapped))
    return entries
