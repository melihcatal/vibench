from google.api_core import datetime_helpers

from observability_client import (
    load_config,
    monitoring_client,
    project_name,
    normalize_metric_name,
)
from observability_models import MetricCompareRequest, series_to_list


def compare_metric_series(metric_type, start_time, end_time, left_filter, right_filter):
    config = load_config()
    client = monitoring_client()
    request = MetricCompareRequest(
        metric_type=normalize_metric_name(metric_type, config),
        start_time=start_time,
        end_time=end_time,
        left_filter=left_filter,
        right_filter=right_filter,
    )
    interval = {
        "start_time": datetime_helpers.to_datetime(request.start_time),
        "end_time": datetime_helpers.to_datetime(request.end_time),
    }
    base = f'metric.type="{request.metric_type}"'
    left = client.list_time_series(
        name=project_name(config),
        filter=f"{base} AND {request.left_filter}",
        interval=interval,
        view=monitoring_client().TimeSeriesView.FULL,
    )
    right = client.list_time_series(
        name=project_name(config),
        filter=f"{base} AND {request.right_filter}",
        interval=interval,
        view=monitoring_client().TimeSeriesView.FULL,
    )
    return {"left": series_to_list(list(left)), "right": series_to_list(list(right))}
