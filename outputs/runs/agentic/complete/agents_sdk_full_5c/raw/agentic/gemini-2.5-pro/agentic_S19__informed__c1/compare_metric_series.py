import time
from typing import Dict, List, Optional
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricSeries, to_metric_series_list

def _fetch_series(
    client: monitoring_v3.MetricServiceClient,
    project_name: str,
    metric_type: str,
    interval: monitoring_v3.TimeInterval,
    dimension_filter: Dict[str, str],
) -> List[MetricSeries]:
    """Helper to fetch a single filtered time series."""
    
    filter_parts = [f'metric.type = "{metric_type}"']
    for key, value in dimension_filter.items():
        filter_parts.append(f'{key} = "{value}"')
    
    request = {
        "name": project_name,
        "filter": " AND ".join(filter_parts),
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
    results = client.list_time_series(request)
    return to_metric_series_list(results)

def compare_metric_series(
    project_id: str,
    metric_type: str,
    minutes_ago: int,
    filter1: Dict[str, str],
    filter2: Dict[str, str],
) -> Dict[str, List[MetricSeries]]:
    """
    Compares metric values for two resources or dimension filters.

    Args:
        project_id: The Google Cloud project ID.
        metric_type: The identifier of the metric.
        minutes_ago: The time window in minutes.
        filter1: The first set of dimension filters.
        filter2: The second set of dimension filters.

    Returns:
        A dictionary with keys 'series1' and 'series2' containing their data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": seconds - (minutes_ago * 60), "nanos": nanos},
        }
    )

    series1 = _fetch_series(client, project_name, metric_type, interval, filter1)
    series2 = _fetch_series(client, project_name, metric_type, interval, filter2)
    
    return {"series1": series1, "series2": series2}

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    proj_id = get_project_id()
    # A metric that can be filtered by disk device
    metric = "compute.googleapis.com/instance/disk/read_bytes_count" 

    # Replace with real instance and device names
    instance_id = "your-instance-id" 
    filters1 = {
        "resource.labels.instance_id": instance_id,
        "metric.labels.device_name": "your-device-name-1" # e.g., 'sda'
    }
    filters2 = {
        "resource.labels.instance_id": instance_id,
        "metric.labels.device_name": "your-device-name-2" # e.g., 'sdb'
    }

    print("Comparing two metric series...")
    try:
        comparison_result = compare_metric_series(proj_id, metric, 30, filters1, filters2)
        
        print("\n--- Series 1 (Filter: {}) ---".format(filters1))
        if not comparison_result["series1"]:
            print("No data found.")
        for s in comparison_result["series1"]:
            print(f"  Points found: {len(s.points)}")

        print("\n--- Series 2 (Filter: {}) ---".format(filters2))
        if not comparison_result["series2"]:
            print("No data found.")
        for s in comparison_result["series2"]:
            print(f"  Points found: {len(s.points)}")
    
    except ValueError as e:
         print(f"Error: {e}. Did you replace the placeholder filter values?")

