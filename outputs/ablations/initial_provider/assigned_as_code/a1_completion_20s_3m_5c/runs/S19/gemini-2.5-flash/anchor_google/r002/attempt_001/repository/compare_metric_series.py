import json

from google.cloud import monitoring_v3
from observability_client import get_metric_service_client
from observability_models import format_time_interval, normalize_time_series_points


def compare_metric_series(payload, config=None):
    config = config or {}
    client = get_metric_service_client()

    project_id = config['project_id']
    metric_type = payload['metric']
    start_time = payload['start_time']
    end_time = payload['end_time']
    filter_1 = payload['filter_1']  # e.g., {"resource.labels.instance_name": "instance-1"}
    filter_2 = payload['filter_2']  # e.g., {"resource.labels.instance_name": "instance-2"}

    def _get_series(dimension_filter):
        filter_str = f"metric.type = {json.dumps(metric_type)}"
        for dim, value in dimension_filter.items():
            filter_str += f" AND {dim} = {json.dumps(value)}"

        series_data = client.list_time_series(request={
            "name": f"projects/{project_id}",
            "filter": filter_str,
            "interval": format_time_interval(start_time, end_time),
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        })
        return normalize_time_series_points(series_data)

    series_1_points = _get_series(filter_1)
    series_2_points = _get_series(filter_2)

    return {"series_1": series_1_points, "series_2": series_2_points}
