from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import create_time_interval, normalize_time_series


def filter_metric_dimensions(
    metric_type, end_time_str, minutes, dimension_key, dimension_value
):
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"
    interval = create_time_interval(end_time_str, minutes)

    query = f'metric.type="{metric_type}" AND resource.labels.{dimension_key}="{dimension_value}"'

    result = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return normalize_time_series(result)
