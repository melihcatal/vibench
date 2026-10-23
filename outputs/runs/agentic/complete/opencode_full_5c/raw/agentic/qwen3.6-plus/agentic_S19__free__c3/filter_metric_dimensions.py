from datetime import datetime
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import MetricsQueryRequest
from observability_client import get_datadog_configuration, validate_time_window
from observability_models import MetricSeries, normalize_datadog_series


def filter_metric_dimensions(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    filter_dimensions: dict[str, str],
    aggregation: str = "avg",
    group_by: list[str] | None = None,
) -> list[MetricSeries]:
    config = get_datadog_configuration()
    validate_time_window(int(start_time.timestamp()), int(end_time.timestamp()))

    query_parts = [metric_name]
    for key, value in sorted(filter_dimensions.items()):
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

    series_list = []
    for raw_series in response.series:
        scope_str = (
            raw_series.scope
            if hasattr(raw_series, "scope") and raw_series.scope
            else ""
        )
        series = normalize_datadog_series(
            {
                "scope": scope_str,
                "pointlist": raw_series.pointlist
                if hasattr(raw_series, "pointlist")
                else [],
            },
            metric_name=metric_name,
            aggregation=aggregation,
        )
        matched = all(
            series.dimensions.get(k) == v for k, v in filter_dimensions.items()
        )
        if matched:
            series_list.append(series)

    return series_list
