from dataclasses import dataclass, asdict
from datetime import datetime, timezone


def normalize_timestamp(value: datetime | None) -> str:
    ts = value or datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc).isoformat()


@dataclass(frozen=True)
class LogEvent:
    message: str
    severity: str = "INFO"
    request_id: str | None = None
    correlation_id: str | None = None
    service: str | None = None
    timestamp: str | None = None

    def to_payload(self) -> dict:
        payload = asdict(self)
        if payload["timestamp"] is None:
            payload["timestamp"] = normalize_timestamp(None)
        return {k: v for k, v in payload.items() if v is not None}
