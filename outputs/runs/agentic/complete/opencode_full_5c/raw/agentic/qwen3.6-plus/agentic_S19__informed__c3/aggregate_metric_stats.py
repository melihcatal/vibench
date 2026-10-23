import os
import time
from typing import Any

import requests

from observability_models import (
    MetricQueryRequest,
    MetricTimeSeries,
    MetricAggregationResult,
    AggregationType,
    build_datadog_query_expression,
    parse_datadog_series_response,
    normalize_timestamps,
)
from observability_client import (
    DatadogConfig,
    load_config,
    make_datadog_request,
    compute_aggregation_from_points,
)

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"


def aggregate_metric_stats(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    tags: list[str] | None = None,
    config: DatadogConfig | None = None,
) -> MetricAggregationResult:
    query_request = MetricQueryRequest(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        aggregation=AggregationType.AVG,
        interval_seconds=interval_seconds,
        tags=tags or [],
    )
    expression = build_datadog_query_expression(
        metric_name=query_request.metric_name,
        aggregation=AggregationType.AVG,
        tags=query_request.tags if query_request.tags else None,
        rollup_seconds=query_request.interval_seconds,
    )
    start, end = normalize_timestamps(
        query_request.start_timestamp, query_request.end_timestamp
    )
    if config is None:
        config = load_config()
    params = {
        "query": expression,
        "from": start,
        "to": end,
    }
    response_data = make_datadog_request("GET", "/query", config=config, params=params)
    time_series = parse_datadog_series_response(response_data, metric_name)
    result = compute_aggregation_from_points(time_series.points, aggregation)
    result.metric_name = metric_name
    result.start_timestamp = start
    result.end_timestamp = end
    result.unit = time_series.unit
    return result


def aggregate_metric_stats_recent(
    metric_name: str,
    window_minutes: int = 60,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    tags: list[str] | None = None,
    config: DatadogConfig | None = None,
) -> MetricAggregationResult:
    now = int(time.time())
    start = now - (window_minutes * 60)
    return aggregate_metric_stats(
        metric_name=metric_name,
        start_timestamp=start,
        end_timestamp=now,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        tags=tags,
        config=config,
    )


def aggregate_all_stats(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    interval_seconds: int = 60,
    tags: list[str] | None = None,
    config: DatadogConfig | None = None,
) -> dict[str, MetricAggregationResult]:
    now = int(time.time()) if end_timestamp == 0 else end_timestamp
    start, end = normalize_timestamps(start_timestamp, now)
    query_request = MetricQueryRequest(
        metric_name=metric_name,
        start_timestamp=start,
        end_timestamp=end,
        aggregation=AggregationType.AVG,
        interval_seconds=interval_seconds,
        tags=tags or [],
    )
    expression = build_datadog_query_expression(
        metric_name=query_request.metric_name,
        aggregation=AggregationType.AVG,
        tags=query_request.tags if query_request.tags else None,
        rollup_seconds=query_request.interval_seconds,
    )
    if config is None:
        config = load_config()
    params = {
        "query": expression,
        "from": start,
        "to": end,
    }
    response_data = make_datadog_request("GET", "/query", config=config, params=params)
    time_series = parse_datadog_series_response(response_data, metric_name)
    results = {}
    for agg_type in AggregationType:
        agg_result = compute_aggregation_from_points(time_series.points, agg_type)
        agg_result.metric_name = metric_name
        agg_result.start_timestamp = start
        agg_result.end_timestamp = end
        agg_result.unit = time_series.unit
        results[agg_type.value] = agg_result
    return results


if __name__ == "__main__":
    metric = os.environ.get("DD_METRIC_NAME", "system.cpu.user")
    window = int(os.environ.get("DD_WINDOW_MINUTES", "60"))
    result = aggregate_metric_stats_recent(metric, window_minutes=window)
    print(f"Metric: {result.metric_name}")
    print(f"Aggregation: {result.aggregation_type.value}")
    print(f"Value: {result.value}")
    print(f"Min: {result.min_value}")
    print(f"Max: {result.max_value}")
    print(f"Avg: {result.avg_value}")
    print(f"Sum: {result.sum_value}")
    print(f"Count: {result.sample_count}")
