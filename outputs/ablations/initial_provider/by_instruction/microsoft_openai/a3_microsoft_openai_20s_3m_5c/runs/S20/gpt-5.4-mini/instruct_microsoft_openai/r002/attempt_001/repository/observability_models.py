import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _compact(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _compact(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_compact(v) for v in value if v is not None]
    if isinstance(value, datetime):
        return _iso(value)
    return value


@dataclass
class LogEvent:
    timestamp: datetime
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return _compact(asdict(self))


@dataclass
class QueryWindow:
    start: datetime
    end: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {"start": _iso(self.start), "end": _iso(self.end)}


@dataclass
class LogQueryRequest:
    severity: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
    window: Optional[QueryWindow] = None
    limit: int = 50

    def to_dict(self) -> Dict[str, Any]:
        payload = {"severity": self.severity, "fields": self.fields, "limit": self.limit}
        if self.window:
            payload["window"] = self.window.to_dict()
        return _compact(payload)


def normalize_events(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        copy = dict(item)
        if isinstance(copy.get("timestamp"), datetime):
            copy["timestamp"] = _iso(copy["timestamp"])
        normalized.append(_compact(copy))
    return normalized


def json_dumps(payload: Dict[str, Any]) -> str:
    return json.dumps(_compact(payload), separators=(",", ":"), sort_keys=True)
