import os
from datetime import datetime, timedelta
from typing import Dict, List
from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQuery, MetricData, TimeSeries


def compare_metric_series(
    project_id: str,
    metric_type: str,
    filter_a: str,  # e.g., 'resource.labels.instance_name = "instance-a"'
    filter_b: str,  # e.g., 'resource.labels.instance_name = "instance-b"'
    minutes: int = 5,
) -> Dict[str, MetricData]:
    """Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    client = GoogleCloudMonitoringClient()

    # Query for filter A
    query_a = MetricQuery(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        filter=filter_a,
        interval_seconds=60,
    )
    data_a = client.query_metric_data(query_a)

    # Query for filter B
    query_b = MetricQuery(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        filter=filter_b,
        interval_seconds=60,
    )
    data_b = client.query_metric_data(query_b)

    return {"series_a": data_a, "series_b": data_b}


# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS and PROJECT_ID are set)
# if __name__ == "__main__":
#     project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
#     metric_type = "compute.googleapis.com/instance/cpu/utilization"
#     filter_a = 'resource.labels.instance_name = "instance-1"'
#     filter_b = 'resource.labels.instance_name = "instance-2"'
#     comparison_data = compare_metric_series(project_id, metric_type, filter_a, filter_b, minutes=10)

#     print("--- Series A ---")
#     for series in comparison_data["series_a"].time_series:
#         print(f"Metric: {series.metric_labels}, Resource: {series.resource_labels}")
#         for point in series.points:
#             print(f"  {point.timestamp}: {point.value}")

#     print("\n--- Series B ---")
#     for series in comparison_data["series_b"].time_series:
#         print(f"Metric: {series.metric_labels}, Resource: {series.resource_labels}")
#         for point in series.points:
#             print(f"  {point.timestamp}: {point.value}")
