import os
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str, metric_type: str, resource_type: str, label_key: str, label_value: str):
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        resource_type: The type of monitored resource (e.g., "gce_instance").
        label_key: The key of the resource label to filter by (e.g., "instance_name").
        label_value: The value of the resource label to filter by.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Define the filter to query metric data
    # This filter specifies the metric type, resource type, and a resource label
    # to filter by. For more complex filters, refer to Google Cloud Monitoring documentation.
    filter_str = (
        f'metric.type = "{metric_type}" AND '
        f'resource.type = "{resource_type}" AND '
        f'resource.labels.{label_key} = "{label_value}"'
    )

    now = client.common.time_interval.now()
    interval = monitoring_v3.TimeInterval(end_time=now, start_time=now - monitoring_v3.TimeInterval(seconds=3600)) # Last 1 hour

    results = client.list_time_series(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    print(f"Metric data for project '{project_id}' filtered by {label_key}={label_value}:")
    for time_series in results:
        print(f"  Metric: {time_series.metric.type}")
        print(f"  Resource: {time_series.resource.type}")
        for label, value in time_series.resource.labels.items():
            print(f"    Resource Label - {label}: {value}")
        for point in time_series.points:
            print(f"    Value: {point.value.double_value if point.value.HasField('double_value') else point.value.int64_value}, Timestamp: {point.interval.end_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Replace with your Google Cloud project ID and desired filter parameters
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # gcloud is authenticated.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    resource_type = "gce_instance"
    label_key = "instance_name"
    label_value = "your-instance-name" # Replace with an actual instance name

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    elif label_value == "your-instance-name":
        print("Please replace 'your-instance-name' with an actual GCE instance name to query.")
    else:
        filter_metric_dimensions(project_id, metric_type, resource_type, label_key, label_value)
