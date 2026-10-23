from __future__ import annotations
import dataclasses
import datetime
from typing import Any, Dict, Optional


@dataclasses.dataclass
class LogEvent:
    timestamp: Optional[datetime.datetime] = None
    level: str = "INFO"
    message: str = ""
    correlation_id: Optional[str] = None
    payload: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        # Convert dataclass to dict for serialization
        data = dataclasses.asdict(self)
        # Ensure timestamp is ISO8601 string if present
        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclasses.dataclass
class LogResponse:
    status_code: int
    body: Any = None
    raw_response: Any = None

    @classmethod
    def from_response(cls, response):
        try:
            body = response.json()
        except Exception:
            body = response.text
        return cls(status_code=response.status_code, body=body, raw_response=response)


@dataclasses.dataclass
class NormalizedLog:
    timestamp: datetime.datetime
    severity: str
    message: str
    correlation_id: Optional[str] = None
    source: str = "unknown"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> NormalizedLog:
        # Convert dict (from any provider) into normalized model
        ts = d.get("timestamp")
        if isinstance(ts, str):
            ts = datetime.datetime.fromisoformat(ts.rstrip("Z"))
        elif isinstance(ts, (int, float)):
            ts = datetime.datetime.utcfromtimestamp(ts)
        return cls(
            timestamp=ts,
            severity=d.get("level") or d.get("severity") or "INFO",
            message=d.get("message") or d.get("log"),
            correlation_id=d.get("correlation_id") or d.get("ddtags"),
        )
