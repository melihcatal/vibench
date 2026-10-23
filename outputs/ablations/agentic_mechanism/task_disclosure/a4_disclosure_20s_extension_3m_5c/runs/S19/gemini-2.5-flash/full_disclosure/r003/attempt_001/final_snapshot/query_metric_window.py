
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import time

def query_metric_window(project_id: str, metric_type: str, minutes: int = 5):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        minutes: The number of minutes to query data for (default 5 minutes).
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos),
        start_time=timestamp_pb2.Timestamp(seconds=(seconds - minutes * 60), nanos=nanos),
    )

    query_filter = f'metric.type = "{metric_type}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    for series in results:
        print(f"Metric: {series.metric.type_}")
        for point in series.points:
            print(f"  Time: {point.interval.end_time.ToDatetime()}, Value: {point.value.double_value}")

if __name__ == '__main__':
    # Replace 'your-project-id' with your actual Google Cloud Project ID
    # Replace 'compute.googleapis.com/instance/cpu/utilization' with the desired metric type
    query_metric_window("your-project-id", "compute.googleapis.com/instance/cpu/utilization", 10)
