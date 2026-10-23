from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    severity: str
    message: str
    fields: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return data


@dataclass(frozen=True)
class LogQuery:
    start_time: datetime
    end_time: datetime
    severity: Optional[str] = None
    field_filters: Optional[Mapping[str, Any]] = None
    limit: int = 100

    def normalize(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "start_time": self.start_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "end_time": self.end_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "limit": self.limit,
        }
        if self.severity:
            payload["severity"] = self.severity.upper()
        if self.field_filters:
            payload["field_filters"] = dict(self.field_filters)
        return payload


@dataclass(frozen=True)
class QueryResult:
    records: List[LogRecord]
    next_token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "records": [record.to_dict() for record in self.records],
            "next_token": self.next_token,
        }


def normalize_fields(fields: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in fields.items():
        if isinstance(value, datetime):
            normalized[key] = value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        else:
            normalized[key] = value
    return normalized


def parse_log_records(items: Iterable[Mapping[str, Any]]) -> List[LogRecord]:
    records: List[LogRecord] = []
    for item in items:
        ts = item.get("timestamp")
        if isinstance(ts, str):
            timestamp = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        elif isinstance(ts, datetime):
            timestamp = ts
        else:
            timestamp = datetime.now(timezone.utc)
        records.append(
            LogRecord(
                timestamp=timestamp,
                severity=str(item.get("severity", "INFO")),
                message=str(item.get("message", "")),
                fields=dict(item.get("fields", {})),
            )
        )
    return records
