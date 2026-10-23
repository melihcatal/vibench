import os
from datetime import datetime, timedelta
from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricQuery, MetricData


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    minutes: int = 60,
    agg_aligner: str = "ALIGN_MEAN",
    agg_reducer: str = "REDUCE_MEAN",
) -> MetricData:
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    query = MetricQuery(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        interval_seconds=60 * minutes,  # Aggregate over the entire window
        aggregation_aligner=agg_aligner,
        aggregation_reducer=agg_reducer,
    )

    client = GoogleCloudMonitoringClient()
    metric_data = client.query_metric_data(query)
    return metric_data


# Example usage (assuming GOOGLE_APPLICATION_CREDENTIALS and PROJECT_ID are set)
# if __name__ == "__main__":
#     project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
#     metric_type = "compute.googleapis.com/instance/cpu/utilization"
#     data = aggregate_metric_stats(project_id, metric_type, minutes=30, agg_aligner="ALIGN_MEAN", agg_reducer="REDUCE_MAX")
#     for series in data.time_series:
#         print(f"Metric: {series.metric_labels}, Resource: {series.resource_labels}")
#         for point in series.points:
#             print(f"  Aggregated Value ({point.timestamp}): {point.value}")
