from observability_client import get_monitoring_client
from google.cloud import monitoring_v3

def query_metric_window(project_id: str, metric_type: str, end_time_seconds: int, duration_seconds: int):
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = monitoring_v3.types.TimeInterval()
    now.end_time.seconds = end_time_seconds
    now.end_time.nanos = 0
    now.start_time.seconds = now.end_time.seconds - duration_seconds
    now.start_time.nanos = 0

    query = f"""
        fetch gce_instance
        | metric {metric_type}
        | within {duration_seconds}s
        | align rate(1m)
        | every 1m
    """

    response = client.query_time_series(
        request={
            "name": project_name,
            "query": query,
        }
    )

    time_series_data = []
    for time_series in response:
        for point in time_series.points:
            time_series_data.append({
                "interval_end": point.interval.end_time.rfc3339(),
                "value": point.value.double_value or point.value.int64_value
            })
    return time_series_data
