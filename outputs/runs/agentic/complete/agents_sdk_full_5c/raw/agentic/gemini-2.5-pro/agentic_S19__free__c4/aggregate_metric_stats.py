import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import normalize_to_models, QueryResult


def get_aggregate_cpu_stats(minutes_ago: int = 60) -> QueryResult:
    """
    Retrieves aggregated (mean) CPU utilization across all instances over a time window.
    """
    client, project_name = get_monitoring_client()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    # Aggregation aligns data points to 5-minute intervals and then calculates the mean
    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": 300},  # 5 minutes
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            "group_by_fields": ["resource.zone"],
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    return normalize_to_models(results)


if __name__ == "__main__":
    if not os.getenv("GCP_PROJECT_ID"):
        print("Skipping example run: GCP_PROJECT_ID is not set.")
    else:
        print("Querying aggregated metric stats...")
        data = get_aggregate_cpu_stats(minutes_ago=30)
        for series in data.series:
            print(f"  Resource (Zone): {series.resource_labels.get('zone', 'N/A')}")
            for point in series.points:
                print(f"    {point.timestamp}: {point.value:.4f}")
        print("Aggregation query complete.")
