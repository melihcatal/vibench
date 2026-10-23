
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import time

def filter_metric_dimensions(project_id: str, metric_type: str, resource_type: str, filter_string: str):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos),
        start_time=timestamp_pb2.Timestamp(seconds=(seconds - 3600), nanos=nanos), # Last hour
    )

    query_filter = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}" AND {filter_string}'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    print(f"Metrics filtered by '{filter_string}':")
    for time_series in results:
        print(time_series)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID, metric type, resource type, and filter string
    # Example:
    # project_id = "your-gcp-project-id"
    # metric_type = "logging.googleapis.com/log_entry_count"
    # resource_type = "global"
    # filter_string = 'resource.labels.project_id = "your-gcp-project-id" AND metric.labels.severity = "ERROR"'
    # filter_metric_dimensions(project_id, metric_type, resource_type, filter_string)
    print("Please replace the placeholder values in the main block with your actual project details.")
    print("Example usage commented out in the script.")
