from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def query_metric_window(project_id: str, metric_type: str, end_time: datetime, minutes: int):
    """
    Queries recent datapoints for a named metric over a time window.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query = f'fetch gce_instance :: {metric_type}' # Example metric type, adjust as needed

    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
    )

    data_points = []
    for page in results.pages:
        for time_series in page.time_series:
            for point in time_series.points:
                data_points.append({
                    "timestamp": point.interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "value": point.value.double_value or point.value.int64_value
                })
    return data_points
