import json

from google.cloud import monitoring_v3
from observability_client import get_metric_service_client
from observability_models import format_time_interval, normalize_time_series_points


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = get_metric_service_client()

    project_id = config['project_id']
    metric_type = payload['metric']
    start_time = payload['start_time']
    end_time = payload['end_time']
    dimension_filters = payload.get('dimension_filters', {}) # e.g., {"resource.labels.instance_name": "my-instance"}

    filter_str = f"metric.type = {json.dumps(metric_type)}"
    for dim, value in dimension_filters.items():
        filter_str += f" AND {dim} = {json.dumps(value)}"

    series = client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": filter_str,
        "interval": format_time_interval(start_time, end_time),
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    points = normalize_time_series_points(series)
    return {"points": points}
