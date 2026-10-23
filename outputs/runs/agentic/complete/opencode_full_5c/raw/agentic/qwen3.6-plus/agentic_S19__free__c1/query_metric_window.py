from datetime import datetime, timedelta
from typing import Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import (
    MetricsQueryRequest as DDQueryRequest,
)

from observability_models import (
    MetricAggregation,
    MetricQueryRequest,
    MetricQueryResponse,
    normalize_datadog_response,
)


DATADOG_API_HOST = "api.datadoghq.com"


def query_metric_window(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
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

    return normalize_datadog_response(raw_response)


def query_recent_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricQueryResponse:
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    return query_metric_window(
        metric_name=metric_name,
        start=start,
        end=end,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        dimensions=dimensions,
    )


def get_metric_datapoints(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> list[tuple[datetime, float]]:
    response = query_metric_window(
        metric_name=metric_name,
        start=start,
        end=end,
        aggregation=aggregation,
        interval_seconds=interval_seconds,
        dimensions=dimensions,
    )
    return response.datapoints
