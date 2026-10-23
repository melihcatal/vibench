import math
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
    MetricStatsResult,
    normalize_datadog_response,
)


DATADOG_API_HOST = "api.datadoghq.com"


def aggregate_metric_stats(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricStatsResult:
    api_key = __import__("os").environ.get("DD_API_KEY")
    app_key = __import__("os").environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        return MetricStatsResult(
            metric_name=metric_name,
            aggregation=aggregation.value,
            start=start,
            end=end,
        )

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST

    query_str = f"{aggregation.value}:{metric_name}"
    if dimensions:
        dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
        query_str = f"{query_str}{{{{{','.join(dim_parts)}}}}}"

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

    response = normalize_datadog_response(raw_response)
    return compute_stats_from_response(response, metric_name, aggregation, start, end)


def compute_stats_from_response(
    response: MetricQueryResponse,
    metric_name: str,
    aggregation: MetricAggregation,
    start: datetime,
    end: datetime,
) -> MetricStatsResult:
    values = [v for _, v in response.datapoints if v is not None]
    if not values:
        return MetricStatsResult(
            metric_name=metric_name,
            aggregation=aggregation.value,
            start=start,
            end=end,
        )

    count = len(values)
    avg = sum(values) / count
    min_val = min(values)
    max_val = max(values)
    sum_val = sum(values)

    sorted_values = sorted(values)
    p50 = _percentile(sorted_values, 50)
    p90 = _percentile(sorted_values, 90)
    p95 = _percentile(sorted_values, 95)
    p99 = _percentile(sorted_values, 99)

    variance = sum((x - avg) ** 2 for x in values) / count if count > 0 else 0
    stddev = math.sqrt(variance)

    return MetricStatsResult(
        metric_name=metric_name,
        aggregation=aggregation.value,
        start=start,
        end=end,
        count=count,
        avg=avg,
        min_val=min_val,
        max_val=max_val,
        sum_val=sum_val,
        p50=p50,
        p90=p90,
        p95=p95,
        p99=p99,
        stddev=stddev,
    )


def _percentile(sorted_values: list[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0
    k = (len(sorted_values) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_values[int(k)]
    d0 = sorted_values[int(f)] * (c - k)
    d1 = sorted_values[int(c)] * (k - f)
    return d0 + d1


def get_metric_summary_stats(
    metric_name: str,
    window_minutes: int = 60,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricStatsResult:
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    return aggregate_metric_stats(
        metric_name=metric_name,
        start=start,
        end=end,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        dimensions=dimensions,
    )
