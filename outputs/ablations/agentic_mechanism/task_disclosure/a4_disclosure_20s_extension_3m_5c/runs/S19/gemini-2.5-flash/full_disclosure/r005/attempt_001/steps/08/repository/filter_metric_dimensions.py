from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def filter_metric_dimensions(project_id: str, metric_type: str, minutes_ago: int, filter_string: str):
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        minutes_ago: How many minutes ago to start querying data from.
        filter_string: The monitoring filter string for resource labels or dimensions.
                       Example: 'resource.labels.instance_name = "my-instance"'

    Returns:
        A list of TimeSeries objects containing the queried metric data.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = timestamp_pb2.Timestamp()
    now.GetCurrentTime()
    start_time = timestamp_pb2.Timestamp()
    start_time.seconds = now.seconds - (minutes_ago * 60)
    start_time.nanos = now.nanos

    interval = monitoring_v3.TimeInterval(end_time=now, start_time=start_time)

    query_filter = f'metric.type = "{metric_type}" AND {filter_string}'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    return list(results)
