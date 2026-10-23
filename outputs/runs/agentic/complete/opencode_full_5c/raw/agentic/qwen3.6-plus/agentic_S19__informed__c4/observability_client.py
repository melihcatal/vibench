import os
import time
import json
from typing import Optional

import requests

from observability_models import (
    MetricQuery,
    MetricComparison,
    MetricWindowResponse,
    MetricAggregationResponse,
    MetricComparisonResponse,
    normalize_query_params,
    normalize_dimensions,
    normalize_aggregation,
    build_metric_series,
)

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"


def get_datadog_api_key() -> str:
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        raise ValueError(
            "DD_API_KEY environment variable is required for Datadog Metrics API"
        )
    return api_key


def get_datadog_app_key() -> str:
    app_key = os.environ.get("DD_APP_KEY")
    if not app_key:
        raise ValueError(
            "DD_APP_KEY environment variable is required for Datadog Metrics API"
        )
    return app_key


def build_datadog_headers() -> dict[str, str]:
    return {
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
        "Content-Type": "application/json",
    }


def query_datadog_metrics(query: MetricQuery) -> MetricWindowResponse:
    url = f"{DATADOG_API_BASE}/query"
    params = normalize_query_params(
        query.metric_name, query.start_ts, query.end_ts, query.interval
    )
    agg_func = normalize_aggregation(query.aggregation)
    dim_tags = normalize_dimensions(query.dimensions)
    tag_filter = ",".join(dim_tags) if dim_tags else ""
    query_str = f"{agg_func}:{query.metric_name}"
    if tag_filter:
        query_str += f"{{{tag_filter}}}"
    params["query"] = query_str
    headers = build_datadog_headers()
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    series_list = []
    for raw_series in data.get("series", []):
        series = build_metric_series(
            query.metric_name,
            raw_series,
            agg_func,
            query.interval,
            query.start_ts,
            query.end_ts,
        )
        series_list.append(series)
    return MetricWindowResponse(series=series_list, query=query, status="ok")


def aggregate_datadog_metrics(query: MetricQuery) -> MetricAggregationResponse:
    url = f"{DATADOG_API_BASE}/query"
    params = normalize_query_params(
        query.metric_name, query.start_ts, query.end_ts, query.interval
    )
    agg_func = normalize_aggregation(query.aggregation)
    dim_tags = normalize_dimensions(query.dimensions)
    tag_filter = ",".join(dim_tags) if dim_tags else ""
    query_str = f"{agg_func}:{query.metric_name}"
    if tag_filter:
        query_str += f"{{{tag_filter}}}"
    params["query"] = query_str
    headers = build_datadog_headers()
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    all_values = []
    for raw_series in data.get("series", []):
        for point in raw_series.get("pointlist", []):
            all_values.append(float(point.get("value", 0.0)))
    if not all_values:
        from observability_models import AggregatedStats

        return MetricAggregationResponse(
            stats=AggregatedStats(
                metric_name=query.metric_name,
                avg=0.0,
                sum_value=0.0,
                min_value=0.0,
                max_value=0.0,
                count=0,
                start_ts=query.start_ts,
                end_ts=query.end_ts,
            ),
            query=query,
            status="ok",
            error_message="No datapoints found",
        )
    from observability_models import AggregatedStats

    sorted_vals = sorted(all_values)
    count = len(sorted_vals)
    avg_val = sum(sorted_vals) / count
    p95_idx = max(0, int(count * 0.95) - 1)
    p99_idx = max(0, int(count * 0.99) - 1)
    stats = AggregatedStats(
        metric_name=query.metric_name,
        avg=round(avg_val, 4),
        sum_value=round(sum(sorted_vals), 4),
        min_value=round(sorted_vals[0], 4),
        max_value=round(sorted_vals[-1], 4),
        count=count,
        p95=round(sorted_vals[p95_idx], 4),
        p99=round(sorted_vals[p99_idx], 4),
        start_ts=query.start_ts,
        end_ts=query.end_ts,
    )
    return MetricAggregationResponse(stats=stats, query=query, status="ok")


def compare_datadog_series(comparison: MetricComparison) -> MetricComparisonResponse:
    url = f"{DATADOG_API_BASE}/query"
    headers = build_datadog_headers()
    agg_func = normalize_aggregation(comparison.aggregation)

    def fetch_series(dimensions: dict[str, str]) -> list:
        params = normalize_query_params(
            comparison.metric_name,
            comparison.start_ts,
            comparison.end_ts,
            comparison.interval,
        )
        dim_tags = normalize_dimensions(dimensions)
        tag_filter = ",".join(dim_tags) if dim_tags else ""
        query_str = f"{agg_func}:{comparison.metric_name}"
        if tag_filter:
            query_str += f"{{{tag_filter}}}"
        params["query"] = query_str
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("series", [])

    raw_a = fetch_series(comparison.series_a)
    raw_b = fetch_series(comparison.series_b)

    series_a = build_metric_series(
        comparison.metric_name,
        raw_a[0] if raw_a else {"pointlist": []},
        agg_func,
        comparison.interval,
        comparison.start_ts,
        comparison.end_ts,
    )
    series_b = build_metric_series(
        comparison.metric_name,
        raw_b[0] if raw_b else {"pointlist": []},
        agg_func,
        comparison.interval,
        comparison.start_ts,
        comparison.end_ts,
    )

    vals_a = [dp.value for dp in series_a.datapoints]
    vals_b = [dp.value for dp in series_b.datapoints]
    avg_a = sum(vals_a) / len(vals_a) if vals_a else 0.0
    avg_b = sum(vals_b) / len(vals_b) if vals_b else 0.0
    delta_avg = round(avg_b - avg_a, 4)
    delta_pct = round(((avg_b - avg_a) / avg_a * 100) if avg_a != 0 else 0.0, 4)

    return MetricComparisonResponse(
        series_a=series_a,
        series_b=series_b,
        comparison=comparison,
        delta_avg=delta_avg,
        delta_pct=delta_pct,
        status="ok",
    )
