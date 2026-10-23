import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


_DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "").rstrip("/")
_DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
_DATABRICKS_METRICS_API = "/api/2.0/preview/metrics/query"


@dataclass
class MetricSeriesQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource_a: Optional[Dict[str, str]] = None
    resource_b: Optional[Dict[str, str]] = None
    filter_a: Optional[str] = None
    filter_b: Optional[str] = None
    aggregation: str = "avg"


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _build_selector(metric_name: str, resource: Optional[Dict[str, str]], dimension_filter: Optional[str]) -> str:
    parts = [f'metric="{metric_name}"']
    if resource:
        for key, value in sorted(resource.items()):
            parts.append(f'{key}="{value}"')
    if dimension_filter:
        parts.append(dimension_filter)
    return "{" + ",".join(parts) + "}"


def _auth_headers() -> Dict[str, str]:
    if not _DATABRICKS_HOST or not _DATABRICKS_TOKEN:
        raise ValueError("DATABRICKS_HOST and DATABRICKS_TOKEN are required")
    return {"Authorization": f"Bearer {_DATABRICKS_TOKEN}", "Content-Type": "application/json"}


def _query_series(selector: str, start_time: datetime, end_time: datetime, aggregation: str) -> List[Dict[str, Any]]:
    url = f"{_DATABRICKS_HOST}{_DATABRICKS_METRICS_API}"
    payload = {
        "query": selector,
        "start_time": _iso(start_time),
        "end_time": _iso(end_time),
        "aggregation": aggregation,
    }
    response = requests.post(url, headers=_auth_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("results", data.get("series", []))


def compare_metric_series(query: MetricSeriesQuery) -> Dict[str, Any]:
    selector_a = _build_selector(query.metric_name, query.resource_a, query.filter_a)
    selector_b = _build_selector(query.metric_name, query.resource_b, query.filter_b)
    series_a = _query_series(selector_a, query.start_time, query.end_time, query.aggregation)
    series_b = _query_series(selector_b, query.start_time, query.end_time, query.aggregation)
    return {
        "provider": "databricks",
        "metric_name": query.metric_name,
        "window": {"start_time": _iso(query.start_time), "end_time": _iso(query.end_time)},
        "series_a": series_a,
        "series_b": series_b,
    }


def compare_metric_series_last_hour(metric_name: str, resource_a: Optional[Dict[str, str]] = None, resource_b: Optional[Dict[str, str]] = None, filter_a: Optional[str] = None, filter_b: Optional[str] = None, aggregation: str = "avg") -> Dict[str, Any]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    return compare_metric_series(
        MetricSeriesQuery(
            metric_name=metric_name,
            start_time=start_time,
            end_time=end_time,
            resource_a=resource_a,
            resource_b=resource_b,
            filter_a=filter_a,
            filter_b=filter_b,
            aggregation=aggregation,
        )
    )
