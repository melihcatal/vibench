from datetime import datetime
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import MetricsQueryRequest
from observability_client import get_datadog_configuration, validate_time_window
from observability_models import (
    MetricAggregatedStats,
    compute_percentile,
    normalize_datadog_series,
)


def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    aggregation: str = "avg",
    dimensions: dict[str, str] | None = None,
) -> MetricAggregatedStats:
    config = get_datadog_configuration()
    validate_time_window(int(start_time.timestamp()), int(end_time.timestamp()))

    query_parts = [metric_name]
    if dimensions:
        for key, value in sorted(dimensions.items()):
            query_parts.append(f"{key}:{value}")
    query_string = " ".join(query_parts)

    body = MetricsQueryRequest(
        from_=int(start_time.timestamp()),
        to=int(end_time.timestamp()),
        query=query_string,
    )

    with ApiClient(config) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.query_metrics(body=body)

    all_values = []
    for raw_series in response.series:
        series = normalize_datadog_series(
            {
                "scope": raw_series.scope
                if hasattr(raw_series, "scope") and raw_series.scope
                else "",
                "pointlist": raw_series.pointlist
                if hasattr(raw_series, "pointlist")
                else [],
            },
            metric_name=metric_name,
            aggregation=aggregation,
        )
        all_values.extend(series.values())

    if not all_values:
        return MetricAggregatedStats(
            metric_name=metric_name,
            aggregation=aggregation,
            start_time=start_time,
            end_time=end_time,
            avg=0.0,
            min=0.0,
            max=0.0,
            sum=0.0,
            count=0,
            p50=0.0,
            p90=0.0,
            p95=0.0,
            p99=0.0,
        )

    return MetricAggregatedStats(
        metric_name=metric_name,
        aggregation=aggregation,
        start_time=start_time,
        end_time=end_time,
        avg=sum(all_values) / len(all_values),
        min=min(all_values),
        max=max(all_values),
        sum=sum(all_values),
        count=len(all_values),
        p50=compute_percentile(all_values, 50),
        p90=compute_percentile(all_values, 90),
        p95=compute_percentile(all_values, 95),
        p99=compute_percentile(all_values, 99),
    )
