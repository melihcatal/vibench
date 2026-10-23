from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def normalize_iso8601(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    return str(value)


def build_log_event(message: str, severity: str = 'INFO', **fields: Any) -> dict[str, Any]:
    event = {'message': message, 'severity': severity.upper(), 'timestamp': normalize_iso8601(fields.pop('timestamp', None))}
    event.update(fields)
    return event


@dataclass
class LogQuery:
    start_time: str
    end_time: str
    severity: str | None = None
    filters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {'start_time': self.start_time, 'end_time': self.end_time, 'filters': dict(self.filters)}
        if self.severity:
            payload['severity'] = self.severity.upper()
        return payload


@dataclass
class LogResult:
    records: list[dict[str, Any]]
    raw: Any = None

    def messages(self) -> list[str]:
        return [str(record.get('message', '')) for record in self.records]
