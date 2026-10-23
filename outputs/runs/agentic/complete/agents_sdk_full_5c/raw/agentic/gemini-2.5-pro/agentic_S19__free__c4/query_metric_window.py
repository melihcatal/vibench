import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import normalize_to_models, QueryResult


def query_recent_cpu_utilization(minutes_ago: int = 20) -> QueryResult:
    """
    Queries the average CPU utilization for all instances over a recent time window.
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

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    return normalize_to_models(results)


if __name__ == "__main__":
    if not os.getenv("GCP_PROJECT_ID"):
        print("Skipping example run: GCP_PROJECT_ID is not set.")
    else:
        print("Querying recent metric data points...")
        data = query_recent_cpu_utilization(minutes_ago=15)
        for series in data.series:
            print(f"  Resource: {series.resource_labels}")
            for point in series.points:
                print(f"    {point.timestamp}: {point.value:.4f}")
        print("Query complete.")
