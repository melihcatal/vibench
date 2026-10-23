import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


_DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


@dataclass
class QueryMetricWindowResponse:
    metric: str
    from_ts: datetime
    to_ts: datetime
    points: List[MetricPoint]
    raw: Dict[str, Any]


def _parse_iso8601(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _coerce_timestamp(value: Any) -> datetime:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        return _parse_iso8601(value)
    raise TypeError(f"Unsupported timestamp type: {type(value)!r}")


def _normalize_series_points(series: Dict[str, Any]) -> List[MetricPoint]:
    points: List[MetricPoint] = []
    for item in series.get("pointlist", []) or []:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        ts_ms, value = item[0], item[1]
        if ts_ms is None or value is None:
            continue
        timestamp = datetime.fromtimestamp(float(ts_ms) / 1000.0, tz=timezone.utc)
        points.append(MetricPoint(timestamp=timestamp, value=float(value)))
    return points


def query_metric_window(metric: str, from_ts: Any = None, to_ts: Any = None, *, interval: Optional[int] = None, tags: Optional[List[str]] = None, limit: Optional[int] = None) -> QueryMetricWindowResponse:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    to_dt = _coerce_timestamp(to_ts) if to_ts is not None else datetime.now(timezone.utc)
    from_dt = _coerce_timestamp(from_ts) if from_ts is not None else (to_dt - timedelta(minutes=15))

    params: Dict[str, Any] = {
        "from": int(from_dt.timestamp()),
        "to": int(to_dt.timestamp()),
        "query": metric,
    }
    if interval is not None:
        params["interval"] = interval
    if tags:
        params["tag_filter"] = ",".join(tags)
    if limit is not None:
        params["page[limit]"] = limit

    response = requests.get(
        f"{_DATADOG_API_BASE}/api/v1/query",
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    series_list = payload.get("series", []) or []
    points: List[MetricPoint] = []
    for series in series_list:
        if isinstance(series, dict):
            points.extend(_normalize_series_points(series))

    points.sort(key=lambda p: p.timestamp)
    return QueryMetricWindowResponse(metric=metric, from_ts=from_dt, to_ts=to_dt, points=points, raw=payload)
