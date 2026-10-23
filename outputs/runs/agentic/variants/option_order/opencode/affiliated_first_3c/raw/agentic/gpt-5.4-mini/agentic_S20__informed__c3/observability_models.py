from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class LogEvent:
    message: str
    service: str
    level: str = "info"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        data = {"message": self.message, "service": self.service, "status": self.level, "timestamp": self.timestamp}
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        if self.request_id:
            data["request_id"] = self.request_id
        data.update(self.fields)
        return data


@dataclass
class LogQuery:
    query: str
    start: str
    end: str
    limit: int = 50

    def to_payload(self) -> Dict[str, Any]:
        return {"query": self.query, "time": {"from": self.start, "to": self.end}, "limit": self.limit}


@dataclass
class LogResult:
    data: List[Dict[str, Any]]
    raw: Dict[str, Any]


def normalize_logs(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append({k: v for k, v in item.items() if v is not None})
    return normalized


def time_range_minutes(minutes: int) -> Dict[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return {"start": start.isoformat().replace("+00:00", "Z"), "end": end.isoformat().replace("+00:00", "Z")}
