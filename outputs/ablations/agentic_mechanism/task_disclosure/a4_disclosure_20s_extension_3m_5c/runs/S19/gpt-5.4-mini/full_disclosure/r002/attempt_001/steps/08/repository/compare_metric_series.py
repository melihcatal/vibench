import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from statistics import mean
from typing import Any, Dict, List, Optional

import requests


DATADOG_API_BASE = "https://api.datadoghq.com"


@dataclass
class CompareMetricSeriesRequest:
    metric_name: str
    minutes: int = 60
    left_filters: Optional[Dict[str, str]] = None
    right_filters: Optional[Dict[str, str]] = None
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


def _fetch_series(query: str, from_ts: int, to_ts: int, api_key: str, app_key: str) -> Dict[str, Any]:
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(
        f"{DATADOG_API_BASE}/api/v1/query",
        params={"from": from_ts, "to": to_ts, "query": query},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _extract_values(payload: Dict[str, Any]) -> List[float]:
    values: List[float] = []
    for item in payload.get("series", []) or []:
        for ts, value in item.get("pointlist", []) or []:
            if ts is None or value is None:
                continue
            values.append(float(value))
    return values


def compare_metric_series(request: CompareMetricSeriesRequest) -> Dict[str, Any]:
    api_key = request.api_key or os.getenv("DD_API_KEY")
    app_key = request.app_key or os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY are required for Datadog metric comparison")

    from_ts, to_ts = _window_bounds(request.minutes, request.end_time)
    left_query = _build_query(request.metric_name, request.aggregation, request.left_filters)
    right_query = _build_query(request.metric_name, request.aggregation, request.right_filters)
    left_payload = _fetch_series(left_query, from_ts, to_ts, api_key, app_key)
    right_payload = _fetch_series(right_query, from_ts, to_ts, api_key, app_key)
    left_values = _extract_values(left_payload)
    right_values = _extract_values(right_payload)
    left_mean = mean(left_values) if left_values else None
    right_mean = mean(right_values) if right_values else None

    comparison: Dict[str, Any] = {
        "metric_name": request.metric_name,
        "window_start": datetime.fromtimestamp(from_ts, tz=timezone.utc).isoformat(),
        "window_end": datetime.fromtimestamp(to_ts, tz=timezone.utc).isoformat(),
        "aggregation": request.aggregation,
        "left": {
            "query": left_query,
            "values": left_values,
            "mean": left_mean,
            "raw": left_payload,
        },
        "right": {
            "query": right_query,
            "values": right_values,
            "mean": right_mean,
            "raw": right_payload,
        },
    }

    if left_mean is not None and right_mean is not None:
        comparison["difference"] = left_mean - right_mean
        comparison["ratio"] = (left_mean / right_mean) if right_mean != 0 else None
    else:
        comparison["difference"] = None
        comparison["ratio"] = None

    return comparison


def compare_metric_series_json(metric_name: str, minutes: int = 60, **kwargs: Any) -> Dict[str, Any]:
    result = compare_metric_series(CompareMetricSeriesRequest(metric_name=metric_name, minutes=minutes, **kwargs))
    return result
