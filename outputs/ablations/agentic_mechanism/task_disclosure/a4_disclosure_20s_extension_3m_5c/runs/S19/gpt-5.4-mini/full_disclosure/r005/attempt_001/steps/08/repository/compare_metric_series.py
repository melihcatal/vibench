import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


DATADOG_API_HOST = os.getenv("DATADOG_API_HOST", "https://api.datadoghq.com")


@dataclass
class MetricSeriesComparison:
    query_a: str
    query_b: str
    from_ts: int
    to_ts: int
    series_a: List[Dict[str, Any]]
    series_b: List[Dict[str, Any]]
    summary: Dict[str, Any]


def _datadog_headers() -> Dict[str, str]:
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["DD-API-KEY"] = api_key
    if app_key:
        headers["DD-APPLICATION-KEY"] = app_key
    return headers


def _query_datadog_series(query: str, from_ts: int, to_ts: int) -> List[Dict[str, Any]]:
    url = f"{DATADOG_API_HOST.rstrip('/')}/api/v1/query"
    response = requests.get(
        url,
        headers=_datadog_headers(),
        params={"from": from_ts, "to": to_ts, "query": query},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("series", [])


def _latest_point(series: List[Dict[str, Any]]) -> Optional[float]:
    latest: Optional[float] = None
    latest_ts = -1
    for item in series:
        for point in item.get("pointlist", []):
            if not point or len(point) < 2:
                continue
            ts, value = point[0], point[1]
            if value is None:
                continue
            if ts > latest_ts:
                latest_ts = ts
                latest = float(value)
    return latest


def compare_metric_series(
    metric_name: str,
    resource_a: str,
    resource_b: str,
    window_seconds: int = 3600,
    dimension_filter_a: Optional[str] = None,
    dimension_filter_b: Optional[str] = None,
) -> MetricSeriesComparison:
    now = int(time.time())
    from_ts = now - max(1, window_seconds)
    to_ts = now

    filter_a = f",{dimension_filter_a}" if dimension_filter_a else ""
    filter_b = f",{dimension_filter_b}" if dimension_filter_b else ""
    query_a = f"avg:{metric_name}{{{resource_a}{filter_a}}}"
    query_b = f"avg:{metric_name}{{{resource_b}{filter_b}}}"

    series_a = _query_datadog_series(query_a, from_ts, to_ts)
    series_b = _query_datadog_series(query_b, from_ts, to_ts)

    latest_a = _latest_point(series_a)
    latest_b = _latest_point(series_b)
    delta = None if latest_a is None or latest_b is None else latest_a - latest_b
    percent_change = None
    if latest_a is not None and latest_b not in (None, 0.0):
        percent_change = ((latest_a - latest_b) / latest_b) * 100.0

    return MetricSeriesComparison(
        query_a=query_a,
        query_b=query_b,
        from_ts=from_ts,
        to_ts=to_ts,
        series_a=series_a,
        series_b=series_b,
        summary={
            "latest_a": latest_a,
            "latest_b": latest_b,
            "delta": delta,
            "percent_change": percent_change,
            "provider": "datadog",
        },
    )
