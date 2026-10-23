import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


_DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class AggregateMetricStatsResponse:
    metric: str
    from_ts: datetime
    to_ts: datetime
    count: int
    min: Optional[float]
    max: Optional[float]
    avg: Optional[float]
    sum: Optional[float]
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


def _extract_series_stats(payload: Dict[str, Any]) -> Dict[str, Optional[float]]:
    series_list = payload.get("series", []) or []
    values = []
    for series in series_list:
        if not isinstance(series, dict):
            continue
        for item in series.get("pointlist", []) or []:
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue
            value = item[1]
            if value is None:
                continue
            values.append(float(value))

    if not values:
        return {"count": 0, "min": None, "max": None, "avg": None, "sum": None}

    total = sum(values)
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": total / len(values),
        "sum": total,
    }


def aggregate_metric_stats(metric: str, from_ts: Any = None, to_ts: Any = None, *, interval: Optional[int] = None, tags: Optional[list[str]] = None) -> AggregateMetricStatsResponse:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    to_dt = _coerce_timestamp(to_ts) if to_ts is not None else datetime.now(timezone.utc)
    from_dt = _coerce_timestamp(from_ts) if from_ts is not None else (to_dt - timedelta(hours=1))

    params: Dict[str, Any] = {
        "from": int(from_dt.timestamp()),
        "to": int(to_dt.timestamp()),
        "query": metric,
    }
    if interval is not None:
        params["interval"] = interval
    if tags:
        params["tag_filter"] = ",".join(tags)

    response = requests.get(
        f"{_DATADOG_API_BASE}/api/v1/query",
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    stats = _extract_series_stats(payload)

    return AggregateMetricStatsResponse(
        metric=metric,
        from_ts=from_dt,
        to_ts=to_dt,
        count=stats["count"] or 0,
        min=stats["min"],
        max=stats["max"],
        avg=stats["avg"],
        sum=stats["sum"],
        raw=payload,
    )
