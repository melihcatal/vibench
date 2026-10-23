import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_metric_window(metric_name, window_minutes=60):
    """
    Query recent datapoints for a named metric over a time window.

    Args:
        metric_name: The name of the metric to query (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        window_minutes: Time window in minutes to query (default: 60)

    Returns:
        List of metric datapoints with timestamps and values
    """
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(now.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            results.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else None,
                    "metric_type": time_series.metric.type,
                    "resource_type": time_series.resource.type,
                    "resource_labels": dict(time_series.resource.labels),
                }
            )

    return results


if __name__ == "__main__":
    sample_metric = "compute.googleapis.com/instance/cpu/utilization"
    try:
        data = query_metric_window(sample_metric, window_minutes=30)
        print(f"Retrieved {len(data)} datapoints for metric: {sample_metric}")
    except Exception as e:
        print(f"Error querying metric: {e}")
