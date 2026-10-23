from datetime import datetime, timedelta
from typing import Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import (
    MetricsQueryRequest as DDQueryRequest,
)

from observability_models import (
    MetricAggregation,
    MetricQueryResponse,
    normalize_datadog_response,
)


DATADOG_API_HOST = "api.datadoghq.com"


def filter_metric_dimensions(
    metric_name: str,
    start: datetime,
    end: datetime,
    dimensions: dict[str, str],
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
) -> MetricQueryResponse:
    api_key = __import__("os").environ.get("DD_API_KEY")
    app_key = __import__("os").environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        return MetricQueryResponse(
            status="error", error="DD_API_KEY and DD_APP_KEY required for Datadog"
        )

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST

    dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
    query_str = f"{aggregation.value}:{metric_name}{{{{{','.join(dim_parts)}}}}}"

    dd_request = DDQueryRequest(
        query=query_str,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )
    if interval_seconds:
        dd_request.interval = interval_seconds

    with ApiClient(config) as api_client:
        metrics_api = MetricsApi(api_client)
        raw_response = metrics_api.query_metrics(body=dd_request)

    return normalize_datadog_response(raw_response)


def filter_by_resource_label(
    metric_name: str,
    resource_key: str,
    resource_value: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
) -> MetricQueryResponse:
    return filter_metric_dimensions(
        metric_name=metric_name,
        start=start,
        end=end,
        dimensions={resource_key: resource_value},
        aggregation=aggregation,
        interval_seconds=interval_seconds,
    )


def filter_by_multiple_dimensions(
    metric_name: str,
    dimension_filters: dict[str, str],
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
) -> MetricQueryResponse:
    return filter_metric_dimensions(
        metric_name=metric_name,
        start=start,
        end=end,
        dimensions=dimension_filters,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
    )


def get_dimension_values_for_metric(
    metric_name: str,
    dimension_key: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
) -> list[str]:
    api_key = __import__("os").environ.get("DD_API_KEY")
    app_key = __import__("os").environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        return []

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST

    query_str = f"{aggregation.value}:{metric_name} by {{{dimension_key}}}"

    dd_request = DDQueryRequest(
        query=query_str,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )

    with ApiClient(config) as api_client:
        metrics_api = MetricsApi(api_client)
        raw_response = metrics_api.query_metrics(body=dd_request)

    values = set()
    for series in raw_response.get("series", []):
        scope = series.get("scope", "")
        if scope:
            parts = scope.strip("{}").split(",")
            for part in parts:
                if ":" in part:
                    k, v = part.split(":", 1)
                    if k.strip() == dimension_key:
                        values.add(v.strip())
    return sorted(values)
