from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


def utc_now():
    return datetime.now(timezone.utc)


def parse_window(minutes=60, end_time=None):
    end = end_time or utc_now()
    start = end - timedelta(minutes=minutes)
    return start, end


def normalize_dimensions(dims):
    return {k: str(v) for k, v in (dims or {}).items() if v is not None}


def normalize_points(points):
    return [
        {"time": p["time"].isoformat(), "value": p["value"]}
        for p in points
    ]


@dataclass
class MetricWindowRequest:
    metric: str
    minutes: int = 60
    dimensions: dict = None
