from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def _isoformat(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    for key in ("timestamp", "time", "start_time", "end_time"):
        if key in normalized and isinstance(normalized[key], datetime):
            normalized[key] = _isoformat(normalized[key])
    return normalized


def normalize_result_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_payload(item) for item in items]


@dataclass
class LogEvent:
    timestamp: datetime
    severity: str
    service: str
    message: str
    fields: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = _isoformat(self.timestamp)
        data.update(self.fields)
        data.pop("fields", None)
        return normalize_payload(data)


@dataclass
class LogQuery:
    start_time: datetime
    end_time: datetime
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "start_time": _isoformat(self.start_time),
            "end_time": _isoformat(self.end_time),
        }
        if self.severity:
            data["severity"] = self.severity
        if self.field_filters:
            data.update(self.field_filters)
        return normalize_payload(data)
