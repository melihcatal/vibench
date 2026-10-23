from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time

def compare_metric_series(
    project_id: str,
    metric_type: str,
    interval_seconds: int,
    filter_a: str,
    filter_b: str,
):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        interval_seconds: The duration of the comparison window in seconds.
        filter_a: The monitoring filter for the first series (e.g., 'resource.type = "gce_instance" AND resource.labels.instance_id = "12345"').
        filter_b: The monitoring filter for the second series.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=seconds, nanos=nanos),
        start_time=Timestamp(seconds=seconds - interval_seconds, nanos=nanos),
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},  # Align data to 1-minute intervals
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    print(f"Fetching data for filter A: {filter_a}")
    series_a = client.list_time_series(
        name=project_name,
        filter=filter_a,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        metric_kind=monitoring_v3.MetricKind.GAUGE,
        value_type=monitoring_v3.ValueType.DOUBLE,
        aggregation=aggregation,
        metric=metric_type, # Explicitly specify metric type here.
    )

    print(f"Fetching data for filter B: {filter_b}")
    series_b = client.list_time_series(
        name=project_name,
        filter=filter_b,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        metric_kind=monitoring_v3.MetricKind.GAUGE,
        value_type=monitoring_v3.ValueType.DOUBLE,
        aggregation=aggregation,
        metric=metric_type, # Explicitly specify metric type here.
    )

    # Process and compare the time series data
    print("\n--- Series A Data ---")
    for ts in series_a:
        print(f"  Metric: {ts.metric.type}")
        print(f"  Resource: {ts.resource.type}, labels: {ts.resource.labels}")
        for point in ts.points:
            print(f"    Value: {point.value.double_value}, Time: {point.interval.end_time.seconds}")

    print("\n--- Series B Data ---")
    for ts in series_b:
        print(f"  Metric: {ts.metric.type}")
        print(f"  Resource: {ts.resource.type}, labels: {ts.resource.labels}")
        for point in ts.points:
            print(f"    Value: {point.value.double_value}, Time: {point.interval.end_time.seconds}")

    # Example comparison (can be extended based on specific needs)
    print("\n--- Comparison Summary ---")
    if len(list(series_a)) > 0 and len(list(series_b)) > 0:
        print("Both series returned data. Further comparison logic can be implemented here.")
    else:
        print("One or both series returned no data.")

if __name__ == "__main__":
    # Example Usage (replace with your actual project, metric, and filters)
    PROJECT_ID = "your-gcp-project-id"  # Replace with your GCP Project ID
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/utilization" # Example metric type
    INTERVAL_SECONDS = 300  # Last 5 minutes

    # Example filters for two different instances
    FILTER_A = '''resource.type = "gce_instance" AND metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_id = "YOUR_INSTANCE_ID_A"'''
    FILTER_B = '''resource.type = "gce_instance" AND metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_id = "YOUR_INSTANCE_ID_B"'''

    # For comparing different dimensions of the same resource, adjust filters like:
    # FILTER_A = '''resource.type = "global" AND metric.type = "logging.googleapis.com/log_entry_count" AND metric.labels.severity = "ERROR"'''
    # FILTER_B = '''resource.type = "global" AND metric.type = "logging.googleapis.com/log_entry_count" AND metric.labels.severity = "WARNING"'''


    print(f"Comparing metric: {METRIC_TYPE} for project: {PROJECT_ID}")
    compare_metric_series(PROJECT_ID, METRIC_TYPE, INTERVAL_SECONDS, FILTER_A, FILTER_B)
