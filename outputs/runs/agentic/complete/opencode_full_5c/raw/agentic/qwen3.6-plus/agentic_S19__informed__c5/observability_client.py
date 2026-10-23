from __future__ import annotations

import os
from typing import Any

import requests

from observability_models import (
    Datapoint,
    MetricQueryRequest,
    MetricQueryResponse,
    MetricSeries,
)


DATADOG_API_BASE = "https://api.datadoghq.com"


def load_datadog_config() -> dict[str, str]:
    api_key = os.environ.get("DD_API_KEY", "")
    app_key = os.environ.get("DD_APP_KEY", "")
    api_base = os.environ.get("DD_SITE", "datadoghq.com")
    if api_base not in ("datadoghq.com", "datadoghq.eu", "ddog-gov.com"):
        api_base = "datadoghq.com"
    return {
        "api_key": api_key,
        "app_key": app_key,
        "api_base": f"https://api.{api_base}",
    }


def build_datadog_headers(config: dict[str, str]) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": config["api_key"],
        "DD-APPLICATION-KEY": config["app_key"],
    }


def execute_datadog_query(
    config: dict[str, str],
    request: MetricQueryRequest,
) -> MetricQueryResponse:
    api_base = config["api_base"]
    headers = build_datadog_headers(config)
    url = f"{api_base}/api/v1/query"
    payload = request.to_payload()
    resp = requests.get(url, headers=headers, params=payload, timeout=30)
    resp.raise_for_status()
    body = resp.json()
    series_list: list[MetricSeries] = []
    for raw_series in body.get("series", []):
        metric_name = raw_series.get("metric", request.metric)
        expression = raw_series.get("expression", payload.get("query", ""))
        scope = raw_series.get("scope", "")
        points_raw = raw_series.get("pointlist", [])
        datapoints = [
            Datapoint(timestamp=int(ts), value=float(val))
            for ts, val in points_raw
            if val is not None
        ]
        series_list.append(
            MetricSeries(
                metric=metric_name,
                expression=expression,
                scope=scope,
                aggregation=request.aggregation,
                points=datapoints,
            )
        )
    return MetricQueryResponse(
        series=series_list,
        query=payload["query"],
        from_ts=request.start_ts,
        to_ts=request.end_ts,
        message=body.get("message", ""),
    )


def execute_datadog_queries_parallel(
    config: dict[str, str],
    requests_list: list[MetricQueryRequest],
) -> list[MetricQueryResponse]:
    results: list[MetricQueryResponse] = []
    for req in requests_list:
        results.append(execute_datadog_query(config, req))
    return results


def compute_stats_from_series(series: MetricSeries) -> dict[str, Any]:
    values = [p.value for p in series.points]
    if not values:
        return {
            "count": 0,
            "avg": 0.0,
            "min": 0.0,
            "max": 0.0,
            "sum": 0.0,
            "p50": 0.0,
            "p90": 0.0,
            "p99": 0.0,
        }
    sorted_vals = sorted(values)
    count = len(sorted_vals)
    avg = sum(sorted_vals) / count
    p50 = sorted_vals[int(count * 0.50)]
    p90 = sorted_vals[min(int(count * 0.90), count - 1)]
    p99 = sorted_vals[min(int(count * 0.99), count - 1)]
    return {
        "count": count,
        "avg": avg,
        "min": min(sorted_vals),
        "max": max(sorted_vals),
        "sum": sum(sorted_vals),
        "p50": p50,
        "p90": p90,
        "p99": p99,
    }
