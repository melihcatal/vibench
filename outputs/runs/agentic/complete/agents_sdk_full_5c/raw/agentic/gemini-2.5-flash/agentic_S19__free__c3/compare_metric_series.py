from observability_client import get_monitoring_client
from google.cloud import monitoring_v3

def compare_metric_series(project_id: str, metric_type: str, end_time_seconds: int, duration_seconds: int,
                          filter_a: str, filter_b: str):
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.types.TimeInterval()
    interval.end_time.seconds = end_time_seconds
    interval.end_time.nanos = 0
    interval.start_time.seconds = interval.end_time.seconds - duration_seconds
    interval.start_time.nanos = 0

    results = {}

    # Query for filter A
    full_filter_a = f'metric.type = "{metric_type}" AND {filter_a}'
    response_a = client.list_time_series(
        name=project_name,
        filter=full_filter_a,
        interval=interval,
        view=monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    data_a = []
    for ts in response_a:
        for point in ts.points:
            data_a.append({
                "resource": ts.resource.labels,
                "metric_labels": ts.metric.labels,
                "value": point.value.double_value or point.value.int64_value,
                "end_time": point.interval.end_time.rfc3339()
            })
    results["series_a"] = data_a

    # Query for filter B
    full_filter_b = f'metric.type = "{metric_type}" AND {filter_b}'
    response_b = client.list_time_series(
        name=project_name,
        filter=full_filter_b,
        interval=interval,
        view=monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    data_b = []
    for ts in response_b:
        for point in ts.points:
            data_b.append({
                "resource": ts.resource.labels,
                "metric_labels": ts.metric.labels,
                "value": point.value.double_value or point.value.int64_value,
                "end_time": point.interval.end_time.rfc3339()
            })
    results["series_b"] = data_b

    return results
