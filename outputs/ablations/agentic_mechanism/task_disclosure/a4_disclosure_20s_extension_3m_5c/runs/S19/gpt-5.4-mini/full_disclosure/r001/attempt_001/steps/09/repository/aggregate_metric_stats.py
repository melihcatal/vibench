import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


@dataclass
class MetricAggregateStats:
    metric_name: str
    start: str
    end: str
    count: int
    min: Optional[float]
    max: Optional[float]
    avg: Optional[float]
    sum: Optional[float]
    dimensions: Dict[str, Any]


def _env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _parse_iso_datetime(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def aggregate_metric_stats(metric_name: str, window_minutes: int = 60, rollup: int = 60) -> MetricAggregateStats:
    api_key = _env("DATADOG_API_KEY")
    app_key = _env("DATADOG_APP_KEY")
    site = os.getenv("DATADOG_SITE", "datadoghq.com")

    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=window_minutes)

    url = f"https://api.{site}/api/v1/query"
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
        "rollup": rollup,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()

    series = payload.get("series", [])
    values = []
    dimensions: Dict[str, Any] = {}
    for item in series:
        scope = item.get("scope", "")
        if scope:
            dimensions.setdefault("scopes", []).append(scope)
        for point in item.get("pointlist", []):
            if not point or len(point) < 2 or point[1] is None:
                continue
            values.append(float(point[1]))

    count = len(values)
    metric_min = min(values) if values else None
    metric_max = max(values) if values else None
    metric_sum = sum(values) if values else None
    metric_avg = (metric_sum / count) if values else None

    return MetricAggregateStats(
        metric_name=metric_name,
        start=_parse_iso_datetime(start.isoformat()).isoformat(),
        end=_parse_iso_datetime(end.isoformat()).isoformat(),
        count=count,
        min=metric_min,
        max=metric_max,
        avg=metric_avg,
        sum=metric_sum,
        dimensions=dimensions,
    )


__all__ = ["MetricAggregateStats", "aggregate_metric_stats"]
