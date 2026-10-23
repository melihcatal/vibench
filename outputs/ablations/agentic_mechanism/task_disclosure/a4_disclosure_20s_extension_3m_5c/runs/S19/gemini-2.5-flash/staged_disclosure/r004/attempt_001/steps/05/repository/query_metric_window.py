from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime

def query_metric_window(project_id: str, metric_type: str, end_time: datetime.datetime, minutes: int = 60):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        end_time: The end time for the query window (datetime object).
        minutes: The duration of the time window in minutes, ending at `end_time`. Defaults to 60 minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - datetime.timedelta(minutes=minutes)

    # Convert datetime objects to protobuf Timestamp objects
    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp,
        start_time=start_timestamp
    )

    query_filter = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    print(f"Metric: {metric_type}")
    for series in response.time_series:
        print(f"  Resource: {series.resource.type}, Labels: {series.resource.labels}")
        for point in series.points:
            point_time = point.interval.end_time.ToDatetime()
            value = point.value.double_value if point.value.HasField("double_value") else point.value.int64_value
            print(f"    Time: {point_time}, Value: {value}")

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    PROJECT_ID = "your-google-cloud-project-id"
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/usage_time" # Example metric
    
    # Query for the last 60 minutes
    query_metric_window(PROJECT_ID, METRIC_TYPE, datetime.datetime.now(datetime.timezone.utc), minutes=60)
