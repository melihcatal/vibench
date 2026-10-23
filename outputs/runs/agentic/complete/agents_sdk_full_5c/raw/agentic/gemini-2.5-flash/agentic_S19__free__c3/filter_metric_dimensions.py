from observability_client import get_monitoring_client
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str, metric_type: str, end_time_seconds: int, duration_seconds: int,
                             filter_str: str):
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.types.TimeInterval()
    interval.end_time.seconds = end_time_seconds
    interval.end_time.nanos = 0
    interval.start_time.seconds = interval.end_time.seconds - duration_seconds
    interval.start_time.nanos = 0

    full_filter = f'metric.type = "{metric_type}" AND {filter_str}'

    response = client.list_time_series(
        name=project_name,
        filter=full_filter,
        interval=interval,
        view=monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView.FULL
    )

    filtered_data = []
    for ts in response:
        for point in ts.points:
            filtered_data.append({
                "resource": ts.resource.labels,
                "metric_labels": ts.metric.labels,
                "value": point.value.double_value or point.value.int64_value,
                "end_time": point.interval.end_time.rfc3339()
            })
    return filtered_data
