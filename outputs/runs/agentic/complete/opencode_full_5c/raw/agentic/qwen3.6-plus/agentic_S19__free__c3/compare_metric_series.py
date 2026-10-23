from datetime import datetime
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import MetricsQueryRequest
from observability_client import get_datadog_configuration, validate_time_window
from observability_models import (
    MetricComparisonResult,
    MetricSeries,
    compute_correlation,
    normalize_datadog_series,
)


def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions_a: dict[str, str],
    dimensions_b: dict[str, str],
    aggregation: str = "avg",
) -> MetricComparisonResult:
    config = get_datadog_configuration()
    validate_time_window(int(start_time.timestamp()), int(end_time.timestamp()))

    def build_query(dims: dict[str, str]) -> str:
        parts = [metric_name]
        for key, value in sorted(dims.items()):
            parts.append(f"{key}:{value}")
        return " ".join(parts)

    query_a = build_query(dimensions_a)
    query_b = build_query(dimensions_b)

    body_a = MetricsQueryRequest(
        from_=int(start_time.timestamp()),
        to=int(end_time.timestamp()),
        query=query_a,
    )
    body_b = MetricsQueryRequest(
        from_=int(start_time.timestamp()),
        to=int(end_time.timestamp()),
        query=query_b,
    )

    with ApiClient(config) as api_client:
        api_instance = MetricsApi(api_client)
        response_a = api_instance.query_metrics(body=body_a)
        response_b = api_instance.query_metrics(body=body_b)

    def extract_first_series(response, dims: dict[str, str]) -> MetricSeries:
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
            return series
        return MetricSeries(
            metric_name=metric_name,
            aggregation=aggregation,
            dimensions=dims,
            points=[],
        )

    series_a = extract_first_series(response_a, dimensions_a)
    series_b = extract_first_series(response_b, dimensions_b)

    values_a = series_a.values()
    values_b = series_b.values()

    avg_a = sum(values_a) / len(values_a) if values_a else 0.0
    avg_b = sum(values_b) / len(values_b) if values_b else 0.0
    max_a = max(values_a) if values_a else 0.0
    max_b = max(values_b) if values_b else 0.0
    min_a = min(values_a) if values_a else 0.0
    min_b = min(values_b) if values_b else 0.0

    diff_avg = avg_a - avg_b
    diff_max = max_a - max_b
    diff_min = min_a - min_b
    correlation = compute_correlation(values_a, values_b)

    return MetricComparisonResult(
        series_a=series_a,
        series_b=series_b,
        diff_avg=diff_avg,
        diff_max=diff_max,
        diff_min=diff_min,
        correlation=correlation,
    )
