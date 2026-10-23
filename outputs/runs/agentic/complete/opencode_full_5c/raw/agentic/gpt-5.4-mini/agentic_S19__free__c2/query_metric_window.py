from google.api_core import datetime_helpers

from observability_client import (
    load_config,
    monitoring_client,
    project_name,
    normalize_metric_name,
)
from observability_models import MetricWindowRequest, series_to_list


def query_metric_window(metric_type, start_time, end_time, filter_expression=None):
    config = load_config()
    client = monitoring_client()
    request = MetricWindowRequest(
        metric_type=normalize_metric_name(metric_type, config),
        start_time=start_time,
        end_time=end_time,
        filter_expression=filter_expression,
    )
    query = f'metric.type="{request.metric_type}"'
    if request.filter_expression:
        query = f"{query} AND {request.filter_expression}"
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
