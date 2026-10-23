import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


GRAPHITE_BASE_URL = os.getenv("GRAPHITE_BASE_URL", "https://graphite.example.com")
GRAPHITE_API_TOKEN = os.getenv("GRAPHITE_API_TOKEN", "")


def _parse_iso8601(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _to_unix_seconds(dt: datetime) -> int:
    return int(dt.timestamp())


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str) -> Dict[str, Any]:
    start_dt = _parse_iso8601(start_time)
    end_dt = _parse_iso8601(end_time)
    if end_dt <= start_dt:
        raise ValueError("end_time must be after start_time")

    url = f"{GRAPHITE_BASE_URL.rstrip('/')}/render"
    params = {
        "target": f"{metric_name}",
        "from": _to_unix_seconds(start_dt),
        "until": _to_unix_seconds(end_dt),
        "format": "json",
    }
    headers = {}
    if GRAPHITE_API_TOKEN:
        headers["Authorization"] = f"Bearer {GRAPHITE_API_TOKEN}"

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()

    values = []
    for series in payload:
        datapoints = series.get("datapoints", [])
        for value, _timestamp in datapoints:
            if value is not None:
                values.append(float(value))

    count = len(values)
    total = sum(values)
    minimum = min(values) if values else None
    maximum = max(values) if values else None
    average = (total / count) if count else None

    return {
        "provider": "graphite",
        "metric_name": metric_name,
        "start_time": start_dt.astimezone(timezone.utc).isoformat(),
        "end_time": end_dt.astimezone(timezone.utc).isoformat(),
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "average": average,
    }
