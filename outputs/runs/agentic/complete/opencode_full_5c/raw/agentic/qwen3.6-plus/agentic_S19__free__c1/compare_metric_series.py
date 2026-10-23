from datetime import datetime, timedelta
from typing import Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import (
    MetricsQueryRequest as DDQueryRequest,
)

from observability_models import (
    MetricAggregation,
    MetricComparisonResult,
    MetricQueryResponse,
    normalize_datadog_response,
)


DATADOG_API_HOST = "api.datadoghq.com"


def compare_metric_series(
    metric_name: str,
    start: datetime,
    end: datetime,
    dimensions_a: dict[str, str],
    dimensions_b: dict[str, str],
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
) -> MetricComparisonResult:
    api_key = __import__("os").environ.get("DD_API_KEY")
    app_key = __import__("os").environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        return MetricComparisonResult(
            series_a_name=_format_series_name(metric_name, dimensions_a),
            series_b_name=_format_series_name(metric_name, dimensions_b),
        )

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST

    query_a = _build_dimension_query(metric_name, dimensions_a, aggregation)
    query_b = _build_dimension_query(metric_name, dimensions_b, aggregation)

    dd_request_a = DDQueryRequest(
        query=query_a,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )
    dd_request_b = DDQueryRequest(
        query=query_b,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )
    if interval_seconds:
        dd_request_a.interval = interval_seconds
        dd_request_b.interval = interval_seconds

    with ApiClient(config) as api_client:
        metrics_api = MetricsApi(api_client)
        raw_a = metrics_api.query_metrics(body=dd_request_a)
        raw_b = metrics_api.query_metrics(body=dd_request_b)

    response_a = normalize_datadog_response(raw_a)
    response_b = normalize_datadog_response(raw_b)

    return _compute_comparison(
        response_a,
        response_b,
        metric_name,
        dimensions_a,
        dimensions_b,
        start,
        end,
    )


def compare_resource_metrics(
    metric_name: str,
    resource_key: str,
    resource_a: str,
    resource_b: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
) -> MetricComparisonResult:
    return compare_metric_series(
        metric_name=metric_name,
        start=start,
        end=end,
        dimensions_a={resource_key: resource_a},
        dimensions_b={resource_key: resource_b},
        aggregation=aggregation,
        interval_seconds=interval_seconds,
    )


def _build_dimension_query(
    metric_name: str,
    dimensions: dict[str, str],
    aggregation: MetricAggregation,
) -> str:
    base = f"{aggregation.value}:{metric_name}"
    if dimensions:
        dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
        base = f"{base}{{{{{','.join(dim_parts)}}}}}"
    return base


def _format_series_name(metric_name: str, dimensions: dict[str, str]) -> str:
    if not dimensions:
        return metric_name
    parts = [f"{k}={v}" for k, v in dimensions.items()]
    return f"{metric_name}[{','.join(parts)}]"


def _compute_comparison(
    response_a: MetricQueryResponse,
    response_b: MetricQueryResponse,
    metric_name: str,
    dimensions_a: dict[str, str],
    dimensions_b: dict[str, str],
    start: datetime,
    end: datetime,
) -> MetricComparisonResult:
    points_a = response_a.datapoints
    points_b = response_b.datapoints

    values_a = [v for _, v in points_a]
    values_b = [v for _, v in points_b]

    min_len = min(len(values_a), len(values_b))
    if min_len > 0:
        values_a = values_a[:min_len]
        values_b = values_b[:min_len]

        mean_a = sum(values_a) / len(values_a)
        mean_b = sum(values_b) / len(values_b)
        mean_diff = mean_a - mean_b

        std_a = (sum((x - mean_a) ** 2 for x in values_a) / len(values_a)) ** 0.5
        std_b = (sum((x - mean_b) ** 2 for x in values_b) / len(values_b)) ** 0.5

        if std_a > 0 and std_b > 0:
            covariance = (
                sum((a - mean_a) * (b - mean_b) for a, b in zip(values_a, values_b))
                / min_len
            )
            correlation = covariance / (std_a * std_b)
        else:
            correlation = 0.0
    else:
        mean_diff = 0.0
        correlation = 0.0

    return MetricComparisonResult(
        series_a_name=_format_series_name(metric_name, dimensions_a),
        series_b_name=_format_series_name(metric_name, dimensions_b),
        series_a=points_a,
        series_b=points_b,
        correlation=correlation,
        mean_diff=mean_diff,
        start=start,
        end=end,
    )
