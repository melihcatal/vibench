
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricSeries, TimeSeriesPoint


def get_series_for_instance(
    project_id: str, instance_id: str, minutes_ago: int = 30
) -> Optional[MetricSeries]:
    """Fetches a specific metric series for a single GCE instance."""
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    interval = monitoring_v3.types.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )
    metric_filter = (
        'metric.type = "compute.googleapis.com/instance/network/received_bytes_count" AND '
        f'resource.labels.instance_id = "{instance_id}"'
    )
    
    # Use an iterator to get results, expecting only one series
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
            "interval": interval,
            "view": monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    try:
        result = next(iter(results))
        points = [
            TimeSeriesPoint(
                timestamp=p.interval.end_time.rfc3339(), value=p.value.int64_value
            )
            for p in result.points
        ]
        return MetricSeries(
            name=result.metric.type,
            labels=dict(result.metric.labels),
            resource_labels=dict(result.resource.labels),
            points=points,
        )
    except StopIteration:
        return None

def compare_instance_network_traffic(
    project_id: str, instance_id_1: str, instance_id_2: str
) -> None:
    """Compares the network traffic of two GCE instances."""
    print(f"Comparing network traffic for '{instance_id_1}' and '{instance_id_2}'...")
    
    series1 = get_series_for_instance(project_id, instance_id_1)
    series2 = get_series_for_instance(project_id, instance_id_2)

    if not series1:
        print(f"Could not retrieve data for instance {instance_id_1}")
        return
    if not series2:
        print(f"Could not retrieve data for instance {instance_id_2}")
        return

    # A simple comparison of the latest point
    if series1.points and series2.points:
        latest_val1 = series1.points[0].value
        latest_val2 = series2.points[0].value
        print(f"Latest received bytes for {instance_id_1}: {latest_val1}")
        print(f"Latest received bytes for {instance_id_2}: {latest_val2}")
        if latest_val1 > latest_val2:
            print(f"Instance {instance_id_1} has higher recent traffic.")
        else:
            print(f"Instance {instance_id_2} has higher or equal recent traffic.")
    else:
        print("One or both series had no data points to compare.")

if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    instance1 = os.environ.get("GCP_INSTANCE_ID_1")
    instance2 = os.environ.get("GCP_INSTANCE_ID_2")
    if not all([gcp_project_id, instance1, instance2]):
        raise ValueError(
            "Please set GOOGLE_CLOUD_PROJECT, GCP_INSTANCE_ID_1, "
            "and GCP_INSTANCE_ID_2 environment variables."
        )
    
    compare_instance_network_traffic(gcp_project_id, instance1, instance2)
