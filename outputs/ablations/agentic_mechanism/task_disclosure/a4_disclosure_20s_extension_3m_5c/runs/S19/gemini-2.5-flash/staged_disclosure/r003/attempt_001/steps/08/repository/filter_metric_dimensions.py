
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str, metric_type: str, resource_type: str, dimension_key: str, dimension_value: str):
    """
    Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/utilization").
        resource_type: The type of the monitored resource (e.g., "gce_instance").
        dimension_key: The key of the resource label or dimension to filter by.
        dimension_value: The value of the resource label or dimension to filter by.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Construct the filter string
    # Example: "metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.type = "gce_instance" AND resource.labels.instance_name = "my-instance""
    filter_string = (
        f'metric.type = "{metric_type}" AND '
        f'resource.type = "{resource_type}" AND '
        f'resource.labels.{dimension_key} = "{dimension_value}"'
    )

    now = client.common.time_interval.TimeInterval()
    now.end_time.seconds = int(time.time())
    now.start_time.seconds = now.end_time.seconds - 3600  # Last hour

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_string,
            "interval": now,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    for series in results:
        print(f"Metric: {series.metric.type}")
        print(f"Resource: {series.resource.type}")
        for label_key, label_value in series.resource.labels.items():
            print(f"  Resource Label: {label_key} = {label_value}")
        for point in series.points:
            print(f"  Point: {point.interval.end_time.ToDatetime()} - Value: {point.value.double_value}")

if __name__ == "__main__":
    import time
    # Replace with your actual project ID, metric type, resource type, and dimension
    PROJECT_ID = "your-gcp-project-id" # IDENTIFYING SIGNAL: Google Cloud Project ID
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/utilization"
    RESOURCE_TYPE = "gce_instance"
    DIMENSION_KEY = "instance_name"  # Example for gce_instance, can be 'zone', 'project_id', etc.
    DIMENSION_VALUE = "your-instance-name" # Replace with your instance name or other dimension value

    print(f"Querying metrics for project: {PROJECT_ID}")
    filter_metric_dimensions(PROJECT_ID, METRIC_TYPE, RESOURCE_TYPE, DIMENSION_KEY, DIMENSION_VALUE)
