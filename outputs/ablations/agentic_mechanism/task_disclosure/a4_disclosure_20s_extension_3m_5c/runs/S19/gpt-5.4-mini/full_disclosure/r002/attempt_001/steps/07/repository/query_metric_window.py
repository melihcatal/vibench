import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


@dataclass
class MetricWindowResult:
    metric: str
    from_ts: int
    to_ts: int
    points: List[MetricPoint]
    raw: Dict[str, Any]


def _parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def _window_bounds(minutes: int, end_time: Optional[datetime] = None) -> tuple[int, int]:
    end = end_time or datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return int(start.timestamp()), int(end.timestamp())


def query_metric_window(
    metric: str,
    minutes: int = 60,
    *,
    aggregator: str = "avg",
    end_time: Optional[datetime] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
) -> MetricWindowResult:
    api_key = api_key or os.getenv("DD_API_KEY")
    app_key = app_key or os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY are required for Datadog metric queries")

    from_ts, to_ts = _window_bounds(minutes, end_time)
    params = {
        "from": from_ts,
        "to": to_ts,
        "query": f"{aggregator}:{metric}{{*}}",
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(f"{DATADOG_API_BASE}/api/v1/query", params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    series = payload.get("series", [])
    points: List[MetricPoint] = []
    for item in series:
        for ts, value in item.get("pointlist", []) or []:
            if ts is None or value is None:
                continue
            points.append(MetricPoint(timestamp=datetime.fromtimestamp(ts, tz=timezone.utc), value=float(value)))
    points.sort(key=lambda p: p.timestamp)
    return MetricWindowResult(metric=metric, from_ts=from_ts, to_ts=to_ts, points=points, raw=payload)


def query_metric_window_json(metric: str, minutes: int = 60, **kwargs: Any) -> Dict[str, Any]:
    result = query_metric_window(metric, minutes, **kwargs)
    return {
        "metric": result.metric,
        "from": result.from_ts,
        "to": result.to_ts,
        "points": [{"timestamp": p.timestamp.isoformat(), "value": p.value} for p in result.points],
        "raw": result.raw,
    }
