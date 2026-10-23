import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class FilterMetricDimensionsRequest:
    metric_name: str
    minutes: int = 60
    filters: Optional[Dict[str, str]] = None
    aggregation: str = "avg"
    end_time: Optional[datetime] = None
    api_key: Optional[str] = None
    app_key: Optional[str] = None


def _window_bounds(minutes: int, end_time: Optional[datetime] = None) -> tuple[int, int]:
    end = end_time or datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return int(start.timestamp()), int(end.timestamp())


def _build_query(metric_name: str, aggregation: str, filters: Optional[Dict[str, str]]) -> str:
    if filters:
        clauses = [f"{key}:{value}" for key, value in sorted(filters.items()) if value is not None]
        selector = ",".join(clauses) if clauses else "*"
    else:
        selector = "*"
    return f"{aggregation}:{metric_name}{{{selector}}}"


def filter_metric_dimensions(request: FilterMetricDimensionsRequest) -> Dict[str, Any]:
    api_key = request.api_key or os.getenv("DD_API_KEY")
    app_key = request.app_key or os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY are required for Datadog metric filtering")

    from_ts, to_ts = _window_bounds(request.minutes, request.end_time)
    params = {
        "from": from_ts,
        "to": to_ts,
        "query": _build_query(request.metric_name, request.aggregation, request.filters),
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(f"{DATADOG_API_BASE}/api/v1/query", params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    series: List[Dict[str, Any]] = payload.get("series", [])

    parsed_series: List[Dict[str, Any]] = []
    for item in series:
        points = []
        for ts, value in item.get("pointlist", []) or []:
            if ts is None or value is None:
                continue
            points.append({"timestamp": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(), "value": float(value)})
        parsed_series.append(
            {
                "scope": item.get("scope"),
                "metric": item.get("metric"),
                "tag_set": item.get("tag_set"),
                "points": points,
            }
        )

    return {
        "metric_name": request.metric_name,
        "query": params["query"],
        "window_start": datetime.fromtimestamp(from_ts, tz=timezone.utc).isoformat(),
        "window_end": datetime.fromtimestamp(to_ts, tz=timezone.utc).isoformat(),
        "series": parsed_series,
        "raw": payload,
    }


def filter_metric_dimensions_json(metric_name: str, minutes: int = 60, **kwargs: Any) -> Dict[str, Any]:
    result = filter_metric_dimensions(FilterMetricDimensionsRequest(metric_name=metric_name, minutes=minutes, **kwargs))
    return result
