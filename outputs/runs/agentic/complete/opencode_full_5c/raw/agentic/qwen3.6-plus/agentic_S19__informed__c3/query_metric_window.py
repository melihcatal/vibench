import os
import time
from typing import Any

import requests

from observability_models import (
    MetricQueryRequest,
    MetricTimeSeries,
    MetricDataPoint,
    AggregationType,
    build_datadog_query_expression,
    parse_datadog_series_response,
    normalize_timestamps,
)
from observability_client import DatadogConfig, load_config, make_datadog_request

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"


def query_metric_window(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    tags: list[str] | None = None,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    query_request = MetricQueryRequest(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        tags=tags or [],
    )
    expression = build_datadog_query_expression(
        metric_name=query_request.metric_name,
        aggregation=query_request.aggregation,
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
    return parse_datadog_series_response(response_data, metric_name)


def query_metric_window_recent(
    metric_name: str,
    window_minutes: int = 60,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    tags: list[str] | None = None,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    now = int(time.time())
    start = now - (window_minutes * 60)
    return query_metric_window(
        metric_name=metric_name,
        start_timestamp=start,
        end_timestamp=now,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        tags=tags,
        config=config,
    )


if __name__ == "__main__":
    metric = os.environ.get("DD_METRIC_NAME", "system.cpu.user")
    window = int(os.environ.get("DD_WINDOW_MINUTES", "60"))
    result = query_metric_window_recent(metric, window_minutes=window)
    print(f"Metric: {result.metric_name}")
    print(f"Expression: {result.expression}")
    print(f"Data points: {len(result.points)}")
    if result.points:
        print(f"First: ts={result.points[0].timestamp}, value={result.points[0].value}")
        print(
            f"Last: ts={result.points[-1].timestamp}, value={result.points[-1].value}"
        )
