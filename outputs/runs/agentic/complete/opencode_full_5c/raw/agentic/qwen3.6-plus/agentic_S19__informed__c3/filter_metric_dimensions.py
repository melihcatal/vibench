import os
import time
from typing import Any

import requests

from observability_models import (
    MetricDimensionFilter,
    MetricTimeSeries,
    MetricDataPoint,
    AggregationType,
    build_datadog_query_expression,
    parse_datadog_series_response,
    normalize_timestamps,
)
from observability_client import (
    DatadogConfig,
    load_config,
    make_datadog_request,
)

DATADOG_API_BASE = "https://api.datadoghq.com/api/v1"


def filter_metric_dimensions(
    metric_name: str,
    start_timestamp: int,
    end_timestamp: int,
    tag_filters: list[str],
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    filter_request = MetricDimensionFilter(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tag_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
    )
    expression = build_datadog_query_expression(
        metric_name=filter_request.metric_name,
        aggregation=filter_request.aggregation,
        tags=filter_request.tag_filters,
        rollup_seconds=filter_request.interval_seconds,
    )
    start, end = normalize_timestamps(
        filter_request.start_timestamp, filter_request.end_timestamp
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


def filter_metric_dimensions_recent(
    metric_name: str,
    tag_filters: list[str],
    window_minutes: int = 60,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    now = int(time.time())
    start = now - (window_minutes * 60)
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_timestamp=start,
        end_timestamp=now,
        tag_filters=tag_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


def filter_by_host(
    metric_name: str,
    host: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    tag_filters = [f"host:{host}"]
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tag_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


def filter_by_environment(
    metric_name: str,
    environment: str,
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    tag_filters = [f"env:{environment}"]
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tag_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


def filter_by_multiple_dimensions(
    metric_name: str,
    dimensions: dict[str, str],
    start_timestamp: int,
    end_timestamp: int,
    aggregation: AggregationType = AggregationType.AVG,
    interval_seconds: int = 60,
    config: DatadogConfig | None = None,
) -> MetricTimeSeries:
    tag_filters = [f"{key}:{value}" for key, value in dimensions.items()]
    return filter_metric_dimensions(
        metric_name=metric_name,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        tag_filters=tag_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        config=config,
    )


if __name__ == "__main__":
    metric = os.environ.get("DD_METRIC_NAME", "system.cpu.user")
    host = os.environ.get("DD_HOST_FILTER", "host:web-server-01")
    window = int(os.environ.get("DD_WINDOW_MINUTES", "60"))
    result = filter_metric_dimensions_recent(
        metric, tag_filters=[host], window_minutes=window
    )
    print(f"Metric: {result.metric_name}")
    print(f"Expression: {result.expression}")
    print(f"Scope: {result.scope}")
    print(f"Data points: {len(result.points)}")
