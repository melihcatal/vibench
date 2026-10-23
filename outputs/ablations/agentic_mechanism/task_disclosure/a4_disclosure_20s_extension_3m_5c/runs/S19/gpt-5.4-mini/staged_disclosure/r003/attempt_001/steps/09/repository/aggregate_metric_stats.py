import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


DATADOG_API_BASE_URL = "https://api.datadoghq.com"


def _to_epoch_seconds(value: Any) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return int(dt.timestamp())
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    raise TypeError("Unsupported time value")


def aggregate_metric_stats(metric: str, start: Any, end: Any, interval: Optional[int] = None, aggregator: str = "avg") -> Dict[str, Any]:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise EnvironmentError("DD_API_KEY and DD_APP_KEY are required")

    start_ts = _to_epoch_seconds(start)
    end_ts = _to_epoch_seconds(end)
    if end_ts <= start_ts:
        raise ValueError("end must be greater than start")

    params = {
        "from": start_ts,
        "to": end_ts,
        "query": metric,
    }
    if interval is not None:
        params["interval"] = interval

    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }

    response = requests.get(f"{DATADOG_API_BASE_URL}/api/v1/query", params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()

    series = payload.get("series", [])
    points = []
    values = []
    for item in series:
        for point in item.get("pointlist", []):
            ts, value = point
            if value is None:
                continue
            points.append({"timestamp": ts, "value": value})
            values.append(value)

    if not values:
        return {
            "metric": metric,
            "start": start_ts,
            "end": end_ts,
            "count": 0,
            "min": None,
            "max": None,
            "sum": 0,
            "avg": None,
            "aggregator": aggregator,
            "points": points,
        }

    total = sum(values)
    return {
        "metric": metric,
        "start": start_ts,
        "end": end_ts,
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "sum": total,
        "avg": total / len(values),
        "aggregator": aggregator,
        "points": points,
    }
