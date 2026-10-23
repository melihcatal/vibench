import os
import time
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    MetricSeries,
    MetricDataPoint,
    AggregatedStatsRequest,
    AggregatedStatsResult,
    DimensionFilterRequest,
    DimensionFilterResponse,
    MetricComparisonRequest,
    MetricComparisonResult,
    normalize_datadog_series,
    compute_aggregated_stats,
    compute_correlation,
)


DATADOG_API_BASE = "https://api.datadoghq.com"
DATADOG_METRICS_QUERY_ENDPOINT = "/api/v1/query"
DATADOG_METRICS_SEARCH_ENDPOINT = "/api/v1/metrics"


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


def get_datadog_site() -> str:
    return os.environ.get("DD_SITE", "datadoghq.com")


def build_datadog_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
    }


def build_datadog_api_url(
    site: Optional[str] = None, path: str = DATADOG_METRICS_QUERY_ENDPOINT
) -> str:
    site = site or get_datadog_site()
    return f"https://api.{site}{path}"


def _datadog_get(url: str, params: dict) -> dict:
    headers = build_datadog_headers()
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _datadog_post(url: str, payload: dict) -> dict:
    headers = build_datadog_headers()
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def build_query_params(request: MetricQueryRequest) -> dict:
    params = {
        "query": f"{request.aggregation.value}:{request.metric_name}{{{request.scope}}}",
        "from": int(request.start_time.timestamp()),
        "to": int(request.end_time.timestamp()),
    }
    if request.rollup:
        params["rollup"] = request.rollup.value
    return params


def parse_datadog_query_response(
    raw: dict, request: MetricQueryRequest
) -> MetricQueryResponse:
    raw_series = raw.get("series", [])
    series = normalize_datadog_series(raw_series)
    return MetricQueryResponse(
        series=series,
        query_time_ms=raw.get("query_time_ms", 0),
        from_ts=raw.get("from_date", int(request.start_time.timestamp())),
        to_ts=raw.get("to_date", int(request.end_time.timestamp())),
    )


def query_metric_window(request: MetricQueryRequest) -> MetricQueryResponse:
    url = build_datadog_api_url(path=DATADOG_METRICS_QUERY_ENDPOINT)
    params = build_query_params(request)
    raw = _datadog_get(url, params)
    return parse_datadog_query_response(raw, request)


def query_aggregated_stats(
    request: AggregatedStatsRequest,
) -> list[AggregatedStatsResult]:
    metric_req = MetricQueryRequest(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        aggregation=request.aggregations[0]
        if request.aggregations
        else MetricAggregation.AVG,
        scope=request.scope,
    )
    response = query_metric_window(metric_req)
    return compute_aggregated_stats(response.series)


def query_filtered_dimensions(
    request: DimensionFilterRequest,
) -> DimensionFilterResponse:
    scope_parts = [f.to_query_string() for f in request.filters]
    scope = " ".join(scope_parts) if scope_parts else "*"
    metric_req = MetricQueryRequest(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        aggregation=request.aggregation,
        scope=scope,
    )
    response = query_metric_window(metric_req)
    filter_expr = (
        " AND ".join(f.to_query_string() for f in request.filters)
        if request.filters
        else "*"
    )
    return DimensionFilterResponse(
        series=response.series,
        query_time_ms=response.query_time_ms,
        filter_expression=filter_expr,
    )


def query_metric_comparison(request: MetricComparisonRequest) -> MetricComparisonResult:
    req_a = MetricQueryRequest(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        aggregation=request.aggregation,
        scope=request.scope_a,
    )
    req_b = MetricQueryRequest(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        aggregation=request.aggregation,
        scope=request.scope_b,
    )
    response_a = query_metric_window(req_a)
    response_b = query_metric_window(req_b)

    series_a = (
        response_a.series[0]
        if response_a.series
        else MetricSeries(
            metric_name=request.metric_name,
            scope=request.scope_a,
            aggregation=request.aggregation.value,
        )
    )
    series_b = (
        response_b.series[0]
        if response_b.series
        else MetricSeries(
            metric_name=request.metric_name,
            scope=request.scope_b,
            aggregation=request.aggregation.value,
        )
    )

    values_a = [p.value for p in series_a.points]
    values_b = [p.value for p in series_b.points]

    n = min(len(values_a), len(values_b))
    if n > 0:
        deltas = [values_a[i] - values_b[i] for i in range(n)]
        delta_mean = sum(deltas) / n
        delta_max = max(deltas)
        delta_min = min(deltas)
        correlation = compute_correlation(values_a, values_b)
    else:
        delta_mean = 0.0
        delta_max = 0.0
        delta_min = 0.0
        correlation = 0.0

    return MetricComparisonResult(
        metric_name=request.metric_name,
        aggregation=request.aggregation.value,
        start_time=request.start_time,
        end_time=request.end_time,
        series_a=series_a,
        series_b=series_b,
        delta_mean=delta_mean,
        delta_max=delta_max,
        delta_min=delta_min,
        correlation=correlation,
    )


def get_default_time_window(minutes: int = 60) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)
    return start, now
