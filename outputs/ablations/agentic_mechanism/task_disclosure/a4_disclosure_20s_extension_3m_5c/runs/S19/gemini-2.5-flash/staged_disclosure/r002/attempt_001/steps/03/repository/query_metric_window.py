from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def query_metric_window(project_id: str, metric_type: str, end_time: datetime.datetime, minutes: int):
    """Queries recent datapoints for a named metric over a time window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        end_time: The end time for the query window.
        minutes: The number of minutes to go back from the end_time.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - datetime.timedelta(minutes=minutes)

    # Convert datetime objects to Timestamp protobuf objects
    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(end_time)
    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp,
        start_time=start_timestamp
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    print(f"Querying metric '{metric_type}' for project '{project_id}' from {start_time} to {end_time}...")

    results = client.list_time_series(request=query_params)

    for time_series in results:
        print(f"Metric: {time_series.metric.type}")
        print(f"Resource: {time_series.resource.type}")
        for point in time_series.points:
            print(f"  Value: {point.value.double_value}, Time: {point.interval.end_time.ToDatetime()}")

if __name__ == "__main__":
    # Example Usage: Replace with your project ID and a valid metric type
    # For example, to get CPU usage time for a GCE instance:
    # project_id = "your-gcp-project-id"
    # metric_type = "compute.googleapis.com/instance/cpu/usage_time"
    # end_time = datetime.datetime.now(datetime.timezone.utc)
    # query_metric_window(project_id, metric_type, end_time, 60) # Last 60 minutes
    print("To run, please uncomment the example usage in __main__ and replace with your project_id and metric_type.")
    print("Ensure you have authenticated with Google Cloud, e.g., using `gcloud auth application-default login`.")
