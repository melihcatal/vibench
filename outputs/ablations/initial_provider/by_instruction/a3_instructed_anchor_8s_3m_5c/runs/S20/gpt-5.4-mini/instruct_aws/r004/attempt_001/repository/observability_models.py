from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_iso8601(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    text = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def epoch_ms(dt: datetime) -> int:
    return int(dt.astimezone(timezone.utc).timestamp() * 1000)


@dataclass
class LogEvent:
    timestamp: datetime
    message: str
    severity: str
    fields: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        data = dict(self.fields)
        data.update({"timestamp": self.timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"), "message": self.message, "severity": self.severity})
        return data


@dataclass
class QueryWindow:
    start_time: datetime
    end_time: datetime
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None


def parse_events(items: List[Dict[str, Any]]) -> List[LogEvent]:
    parsed: List[LogEvent] = []
    for item in items:
        timestamp = item.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        elif timestamp is None:
            timestamp = datetime.now(timezone.utc)
        fields = {k: v for k, v in item.items() if k not in {"timestamp", "message", "severity"}}
        parsed.append(LogEvent(timestamp=timestamp, message=str(item.get("message", "")), severity=str(item.get("severity", "INFO")), fields=fields))
    return parsed
