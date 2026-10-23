from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import datetime

def filter_metric_dimensions(project_id: str):
    """Queries metric data filtered by resource labels or dimensions."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now()
    end_time = Timestamp()
    end_time.FromDatetime(now)
    start_time = Timestamp()
    start_time.FromDatetime(now - datetime.timedelta(minutes=5))

    interval = monitoring_v3.TimeInterval(
        end_time=end_time,
        start_time=start_time
    )

    # Example filter: Get CPU utilization for GCE instances in a specific zone.
    # Replace with your desired metric type, resource type, and labels.
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    resource_type = "gce_instance"
    zone = "us-central1-a"  # Replace with your desired zone or remove if not needed for your filter

    # Constructing the filter string
    # For more complex filters, refer to Google Cloud Monitoring filtering documentation:
    # https://cloud.google.com/monitoring/api/v3/filters
    metric_filter = (
        f'metric.type = "{metric_type}" AND '
        f'resource.type = "{resource_type}" AND '
        f'resource.label.zone = "{zone}"'
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    print(f"Metric data filtered by dimensions for project: {project_id}")
    for time_series in results:
        print(f"  Metric: {time_series.metric.type}")
        print(f"  Resource Labels: {time_series.resource.labels}")
        print(f"  Metric Labels: {time_series.metric.labels}")
        for point in time_series.points:
            print(f"    Value: {point.value.double_value}, Time: {point.interval.end_time.ToDatetime()}")

if __name__ == "__main__":
    # Replace "your-gcp-project-id" with your actual Google Cloud Project ID
    # Ensure you have authenticated with gcloud and have the monitoring.timeSeries.list permission
    filter_metric_dimensions("your-gcp-project-id")
