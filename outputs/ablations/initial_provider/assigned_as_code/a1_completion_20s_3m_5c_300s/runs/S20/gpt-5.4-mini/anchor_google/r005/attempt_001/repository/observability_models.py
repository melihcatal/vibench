from dataclasses import dataclass
from datetime import datetime, timezone


def to_rfc3339(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return value


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


@dataclass
class LogQueryRequest:
    severity: str = None
    start_time: str = None
    end_time: str = None
    field: str = None
    value: str = None


@dataclass
class LogWriteResponse:
    submitted: bool
