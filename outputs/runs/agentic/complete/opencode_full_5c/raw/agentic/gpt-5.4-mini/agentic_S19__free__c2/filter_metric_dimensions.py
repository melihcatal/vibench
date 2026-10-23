from google.api_core import datetime_helpers

from observability_client import (
    load_config,
    monitoring_client,
    project_name,
    normalize_metric_name,
)
from observability_models import MetricFilterRequest, series_to_list


def filter_metric_dimensions(metric_type, start_time, end_time, dimension_filter):
    config = load_config()
    client = monitoring_client()
    request = MetricFilterRequest(
        metric_type=normalize_metric_name(metric_type, config),
        start_time=start_time,
        end_time=end_time,
        dimension_filter=dimension_filter,
    )
    dimension_query = " AND ".join(
        [
            f'metric.labels.{key}="{value}"'
            for key, value in request.dimension_filter.items()
        ]
    )
    query = f'metric.type="{request.metric_type}"'
    if dimension_query:
        query = f"{query} AND {dimension_query}"
    interval = {
        "start_time": datetime_helpers.to_datetime(request.start_time),
        "end_time": datetime_helpers.to_datetime(request.end_time),
    }
    results = client.list_time_series(
        name=project_name(config),
        filter=query,
        interval=interval,
        view=monitoring_client().TimeSeriesView.FULL,
    )
    return series_to_list(list(results))
