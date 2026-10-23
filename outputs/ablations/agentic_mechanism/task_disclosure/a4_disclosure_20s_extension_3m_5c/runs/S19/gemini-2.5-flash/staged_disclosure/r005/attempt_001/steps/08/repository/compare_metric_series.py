from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def compare_metric_series(
    project_id: str,
    metric_type: str,
    resource_type: str,
    filter_a: str,
    filter_b: str,
    start_time_str: str,
    end_time_str: str,
):
    """Compares metric values for two different filters over the same time window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The metric type to query (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        resource_type: The resource type (e.g., "gce_instance").
        filter_a: The monitoring filter for the first series (e.g., 'metric.labels.instance_name="instance-1"').
        filter_b: The monitoring filter for the second series (e.g., 'metric.labels.instance_name="instance-2"').
        start_time_str: Start time in RFC3339 format (e.g., "2023-01-01T00:00:00Z").
        end_time_str: End time in RFC3339 format (e.g., "2023-01-01T01:00:00Z").
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = datetime.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    end_time = datetime.datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))

    # Prepare time interval
    interval = monitoring_v3.TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(end_time.timestamp())),
    )

    def fetch_time_series(metric_filter: str):
        return client.list_time_series(
            name=project_name,
            filter=f'metric.type = "{metric_type}" AND resource.type = "{resource_type}" AND {metric_filter}',
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

    print(f"Fetching data for filter A: {filter_a}")
    time_series_a = list(fetch_time_series(filter_a))
    print(f"Fetching data for filter B: {filter_b}")
    time_series_b = list(fetch_time_series(filter_b))

    print("\n--- Metric Series A ---")
    if not time_series_a:
        print("No data found for series A.")
    for series in time_series_a:
        print(f"Metric: {series.metric.type}, Resource: {series.resource.type}, Labels: {series.metric.labels}, {series.resource.labels}")
        for point in series.points:
            print(f"  Value: {point.value.double_value}, Time: {point.interval.end_time.isoformat()}")

    print("\n--- Metric Series B ---")
    if not time_series_b:
        print("No data found for series B.")
    for series in time_series_b:
        print(f"Metric: {series.metric.type}, Resource: {series.resource.type}, Labels: {series.metric.labels}, {series.resource.labels}")
        for point in series.points:
            print(f"  Value: {point.value.double_value}, Time: {point.interval.end_time.isoformat()}")

    # Basic comparison (you can extend this with more sophisticated logic)
    print("\n--- Comparison Summary ---")
    if len(time_series_a) > 0 and len(time_series_b) > 0:
        print("Both series have data. Further comparison logic can be implemented here.")
        # Example: Compare average values if applicable
        avg_a = sum([p.value.double_value for s in time_series_a for p in s.points]) / sum([len(s.points) for s in time_series_a]) if sum([len(s.points) for s in time_series_a]) > 0 else 0
        avg_b = sum([p.value.double_value for s in time_series_b for p in s.points]) / sum([len(s.points) for s in time_series_b]) if sum([len(s.points) for s in time_series_b]) > 0 else 0
        print(f"Average for Series A: {avg_a:.2f}")
        print(f"Average for Series B: {avg_b:.2f}")
    else:
        print("One or both series have no data, making direct comparison difficult.")

if __name__ == "__main__':
    # Replace with your actual project ID and desired parameters
    PROJECT_ID = "your-gcp-project-id"  # e.g., "my-gcp-project"
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/usage_time"
    RESOURCE_TYPE = "gce_instance"
    # Example filters for two different instances
    FILTER_A = 'metric.labels.instance_name="instance-1"'
    FILTER_B = 'metric.labels.instance_name="instance-2"'
    START_TIME = "2023-10-27T00:00:00Z"
    END_TIME = "2023-10-27T01:00:00Z"

    if PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud project ID.")
        print("Also, ensure you have set up authentication (e.g., gcloud auth application-default login).")
    else:
        compare_metric_series(PROJECT_ID, METRIC_TYPE, RESOURCE_TYPE, FILTER_A, FILTER_B, START_TIME, END_TIME)
