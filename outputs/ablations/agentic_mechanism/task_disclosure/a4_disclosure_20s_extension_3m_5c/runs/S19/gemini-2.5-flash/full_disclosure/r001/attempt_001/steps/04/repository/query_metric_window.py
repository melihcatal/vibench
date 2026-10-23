from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime

def query_metric_window(project_id: str, metric_type: str, minutes_ago: int = 5):
    """
    Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        minutes_ago: The number of minutes from now to query data for. Defaults to 5 minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = timestamp_pb2.Timestamp()
    end_time.FromDatetime(now)

    start_time = timestamp_pb2.Timestamp()
    start_time.FromDatetime(now - datetime.timedelta(minutes=minutes_ago))

    interval = monitoring_v3.TimeInterval(
        end_time=end_time,
        start_time=start_time,
    )

    query = f"metric.type=\"{metric_type}\""

    results = client.list_time_series(
        name=project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series_data = []
    for ts in results:
        for point in ts.points:
            time_series_data.append({
                "metric": ts.metric.type,
                "value": point.value.double_value if point.value.HasField("double_value") else point.value.int64_value,
                "timestamp": point.interval.end_time.isoformat(),
                "resource_labels": {k: v for k, v in ts.resource.labels.items()},
                "metric_labels": {k: v for k, v in ts.metric.labels.items()},
            })
    return time_series_data
