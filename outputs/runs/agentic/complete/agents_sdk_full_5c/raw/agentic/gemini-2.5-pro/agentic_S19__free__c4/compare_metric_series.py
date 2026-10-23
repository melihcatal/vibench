import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client

def fetch_series(client, project_name, filter_str, interval) -> List[Dict]:
    """Helper to fetch and parse a single time series."""
    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    series_data = []
    for series in response.time_series:
        for point in series.points:
            value = getattr(point.value, 'double_value', getattr(point.value, 'int64_value', 0))
            series_data.append({
                "timestamp": point.interval.end_time.isoformat(),
                "value": value
            })
    return series_data


def compare_instance_cpu(
    instance_id_a: str,
    instance_id_b: str,
    minutes_ago: int = 60,
) -> Dict[str, List[Dict]]:
    """
    Compares the CPU utilization of two different GCE instances over the same time window.
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

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_a = f'metric.type = "{metric_type}" AND resource.labels.instance_id = "{instance_id_a}"'
    filter_b = f'metric.type = "{metric_type}" AND resource.labels.instance_id = "{instance_id_b}"'

    series_a = fetch_series(client, project_name, filter_a, interval)
    series_b = fetch_series(client, project_name, filter_b, interval)

    return {
        instance_id_a: series_a,
        instance_id_b: series_b,
    }


if __name__ == "__main__":
    if not (os.getenv("GCP_PROJECT_ID") and os.getenv("GCP_INSTANCE_A_ID") and os.getenv("GCP_INSTANCE_B_ID")):
        print("Skipping example: Set GCP_PROJECT_ID, GCP_INSTANCE_A_ID, and GCP_INSTANCE_B_ID.")
    else:
        instance_a = os.environ["GCP_INSTANCE_A_ID"]
        instance_b = os.environ["GCP_INSTANCE_B_ID"]
        print(f"Comparing CPU utilization for '{instance_a}' and '{instance_b}'...")
        
        comparison_data = compare_instance_cpu(instance_a, instance_b, minutes_ago=30)
        
        print(f"\nResults for {instance_a}:")
        if comparison_data[instance_a]:
            for point in comparison_data[instance_a][:5]: # Print first 5 points
                print(f"  {point['timestamp']}: {point['value']:.4f}")
        else:
            print("  No data found.")

        print(f"\nResults for {instance_b}:")
        if comparison_data[instance_b]:
            for point in comparison_data[instance_b][:5]: # Print first 5 points
                print(f"  {point['timestamp']}: {point['value']:.4f}")
        else:
            print("  No data found.")

        print("\nComparison complete.")
