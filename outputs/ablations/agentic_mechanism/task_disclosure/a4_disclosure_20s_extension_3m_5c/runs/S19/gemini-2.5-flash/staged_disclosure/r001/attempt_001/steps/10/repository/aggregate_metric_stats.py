import os
from google.cloud import monitoring_v3

def get_aggregated_metric_stats(
    project_id: str,
    metric_type: str,
    start_time: str,
    end_time: str,
    interval_seconds: int = 60,
    reducer: monitoring_v3.Aggregation.Reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
):
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        start_time: Start time for the query in RFC3339 format (e.g., "2023-01-01T00:00:00Z").
        end_time: End time for the query in RFC3339 format (e.g., "2023-01-01T01:00:00Z").
        interval_seconds: The sampling period in seconds for the aggregation.
        reducer: The Aligner operation to apply to the data. Defaults to REDUCE_MEAN.
        aligner: The Reducer operation to apply to the data. Defaults to ALIGN_MEAN.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(monitoring_v3.helpers.parse_rfc3339(start_time).timestamp())},
        end_time={"seconds": int(monitoring_v3.helpers.parse_rfc3339(end_time).timestamp())},
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": interval_seconds},
        per_series_aligner=aligner,
        cross_series_reducer=reducer,
        group_by_fields=["resource.zone"], # Example grouping
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    print(f"Aggregated Metric Stats for {metric_type}:")
    for series in results:
        print(series)

if __name__ == "__main__":
    # Replace with your actual project ID and metric type
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    METRIC_TYPE = "compute.googleapis.com/instance/cpu/usage_time"
    START_TIME = "2023-10-26T00:00:00Z"
    END_TIME = "2023-10-26T01:00:00Z"

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        get_aggregated_metric_stats(PROJECT_ID, METRIC_TYPE, START_TIME, END_TIME)
