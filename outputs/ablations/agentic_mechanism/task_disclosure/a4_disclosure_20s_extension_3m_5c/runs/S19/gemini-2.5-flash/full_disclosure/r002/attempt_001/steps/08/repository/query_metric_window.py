from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def query_metric_window(project_id: str, metric_name: str, end_time_seconds: int, duration_seconds: int):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_name: The full metric name, e.g., "compute.googleapis.com/instance/cpu/utilization".
        end_time_seconds: The end of the time window in Unix timestamp seconds.
        duration_seconds: The duration of the time window in seconds.

    Returns:
        A list of datapoints.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Prepare time interval
    interval = monitoring_v3.TimeInterval()
    end_time = timestamp_pb2.Timestamp()
    end_time.seconds = end_time_seconds
    interval.end_time = end_time
    interval.start_time.seconds = end_time_seconds - duration_seconds

    # Prepare metric query
    query = f"fetch gce_instance :: {metric_name}" # Example filter for GCE instance metrics

    # Create request
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    response = client.list_time_series(request=request)

    datapoints = []
    for series in response:
        for point in series.points:
            datapoints.append({
                "value": point.value.double_value,
                "timestamp": point.interval.end_time.seconds
            })
    return datapoints
