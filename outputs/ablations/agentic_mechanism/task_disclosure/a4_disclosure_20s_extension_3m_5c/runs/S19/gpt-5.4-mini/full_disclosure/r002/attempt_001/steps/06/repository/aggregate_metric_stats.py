import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


@dataclass
class AggregateMetricStatsRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregation: str = "avg"
    resource_filter: Optional[str] = None


def _isoformat(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def retrieve_aggregated_metric_stats(request: AggregateMetricStatsRequest) -> Dict[str, Any]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    url = f"https://api.{site}/api/v1/query"
    query = request.metric_name
    if request.resource_filter:
        query = f"{query}{{{request.resource_filter}}}"

    params = {
        "from": int(request.start_time.timestamp()),
        "to": int(request.end_time.timestamp()),
        "query": f"{request.aggregation}:{query}",
    }
    headers = {"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key}
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    series = payload.get("series", [])
    points = []
    for item in series:
        for point in item.get("pointlist", []):
            ts_ms, value = point
            if value is not None:
                points.append({"timestamp": datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat(), "value": value})

    values = [p["value"] for p in points]
    stats = {
        "metric_name": request.metric_name,
        "aggregation": request.aggregation,
        "window_start": _isoformat(request.start_time),
        "window_end": _isoformat(request.end_time),
        "point_count": len(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "avg": (sum(values) / len(values)) if values else None,
        "series": series,
        "points": points,
    }
    return stats


def build_default_request(metric_name: str, minutes: int = 60, aggregation: str = "avg") -> AggregateMetricStatsRequest:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return AggregateMetricStatsRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, aggregation=aggregation)
