from dataclasses import dataclass
from datetime import datetime, timezone


def normalize_timestamp(value):
    if value is None:
        return datetime.now(timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(seconds, tz=timezone.utc)
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def build_log_event(message, severity="INFO", **fields):
    event = {"message": message, "severity": severity}
    event.update(fields)
    return event


@dataclass
class LogQueryWindow:
    start_time: datetime
    end_time: datetime


@dataclass
class LogFilter:
    field: str
    value: str
