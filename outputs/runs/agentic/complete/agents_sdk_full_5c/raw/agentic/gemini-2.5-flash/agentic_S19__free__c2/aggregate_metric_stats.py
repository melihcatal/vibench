import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    duration_minutes: int = 60,
    aggregation_period_seconds: int = 300, # 5 minutes
    alignment_period_seconds: int = 60 # 1 minute
):
    """Retrieves aggregated statistics for a metric over a time window."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": alignment_period_seconds},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.instance_id"], # Example: group by instance
    )

    query_filter = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for ts in response.time_series:
        for point in ts.points:
            aggregated_data.append(
                {
                    "metric": ts.metric.type,
                    "resource_labels": dict(ts.resource.labels),
                    "value": point.value.double_value or point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                }
            )
    return aggregated_data

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID and metric type
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # aggregated_stats = aggregate_metric_stats(
    #     PROJECT_ID,
    #     "compute.googleapis.com/instance/cpu/utilization",
    #     datetime.utcnow(),
    #     duration_minutes=30
    # )
    # for stat in aggregated_stats:
    #     print(stat)
    pass
