# Local helper: request/response normalization models
from dataclasses import dataclass
import datetime


@dataclass
class LogEvent:
    event: str
    metadata: dict
    timestamp: int  # epoch ms


@dataclass
class LogSearchResult:
    event: str
    metadata: dict
    timestamp: datetime.datetime  # parsed datetime


@dataclass
class LogQueryParams:
    severity: str = "ERROR"
    start_relative: str = "15m"
    field_filter: str = ""


# Helper to convert UTC datetime to epoch ms (used in queries)
import time


def to_epoch_ms(dt: datetime.datetime) -> int:
    """Convert datetime (assumed UTC) to epoch milliseconds."""
    return int(dt.timestamp() * 1000)


# Example: normalize incoming dict payload to LogEvent


def normalize_event(raw: dict) -> LogEvent:
    return LogEvent(
        event=raw.get("event"),
        metadata=raw.get("metadata", {}),
        timestamp=raw.get("timestamp"),
    )
