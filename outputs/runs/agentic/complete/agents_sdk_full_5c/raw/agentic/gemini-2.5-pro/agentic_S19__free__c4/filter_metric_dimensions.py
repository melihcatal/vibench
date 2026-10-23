import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import normalize_to_models, QueryResult


def get_metrics_for_instance(instance_id: str, zone: str, minutes_ago: int = 30) -> QueryResult:
    """
    Queries metric data for a specific GCE instance, filtered by resource labels.
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

    # Filter by both metric type and a resource label (instance_id)
    metric_filter = (
        'metric.type = "compute.googleapis.com/instance/cpu/utilization" AND '
        f'resource.labels.instance_id = "{instance_id}" AND '
        f'resource.labels.zone = "{zone}"'
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    return normalize_to_models(results)


if __name__ == "__main__":
    if not (os.getenv("GCP_PROJECT_ID") and os.getenv("GCP_TEST_INSTANCE_ID") and os.getenv("GCP_TEST_ZONE")):
        print("Skipping example: Set GCP_PROJECT_ID, GCP_TEST_INSTANCE_ID, and GCP_TEST_ZONE.")
    else:
        test_instance_id = os.environ["GCP_TEST_INSTANCE_ID"]
        test_zone = os.environ["GCP_TEST_ZONE"]
        print(f"Querying metrics for instance '{test_instance_id}' in zone '{test_zone}'...")
        data = get_metrics_for_instance(
            instance_id=test_instance_id,
            zone=test_zone,
            minutes_ago=20
        )
        if not data.series:
            print("  No data returned. The instance may be inactive or have no data for the period.")
        for series in data.series:
            print(f"  Resource Labels: {series.resource_labels}")
            for point in series.points:
                print(f"    {point.timestamp}: {point.value:.4f}")
        print("Filtered query complete.")
