import os
from datetime import datetime, timedelta
from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQuery, MetricData


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    resource_label_filter: str,  # e.g., 'resource.labels.instance_name = "my-instance"'
    minutes: int = 5,
) -> MetricData:
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    query = MetricQuery(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        filter=resource_label_filter,
        interval_seconds=60,
    )

    client = GoogleCloudMonitoringClient()
    metric_data = client.query_metric_data(query)
    return metric_data


# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS and PROJECT_ID are set)
# if __name__ == "__main__":
#     project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
#     metric_type = "compute.googleapis.com/instance/cpu/utilization"
#     instance_name = "your-instance-name"
#     resource_filter = f'resource.labels.instance_name = "{instance_name}"'
#     data = filter_metric_dimensions(project_id, metric_type, resource_filter, minutes=10)
#     for series in data.time_series:
#         print(f"Metric: {series.metric_labels}, Resource: {series.resource_labels}")
#         for point in series.points:
#             print(f"  {point.timestamp}: {point.value}")
