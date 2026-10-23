
from datetime import datetime, timedelta
from typing import Dict
from google.cloud import monitoring_v3

from observability_client import get_monitoring_client, get_project_name

def fetch_series_for_comparison(
    metric_type: str,
    filter_str: str,
    minutes_ago: int
) -> list:
    """Helper to fetch a single time series."""
    client = get_monitoring_client()
    project_name = get_project_name()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    full_filter = f'metric.type = "{metric_type}" AND {filter_str}'
    
    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": full_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return list(response)

def compare_two_metric_series(
    metric_type: str,
    filter1: str,
    filter2: str,
    minutes_ago: int = 60
) -> Dict[str, list]:
    """
    Fetches two metric series for comparison based on different filters.

    Args:
        metric_type: The base metric to query.
        filter1: The filter for the first series (e.g., 'metric.labels.instance_name = "instance-a"').
        filter2: The filter for the second series (e.g., 'metric.labels.instance_name = "instance-b"').
        minutes_ago: The time window in minutes.

    Returns:
        A dictionary containing the two fetched series.
    """
    series1 = fetch_series_for_comparison(metric_type, filter1, minutes_ago)
    series2 = fetch_series_for_comparison(metric_type, filter2, minutes_ago)

    return {
        "series_a": series1,
        "series_b": series2,
    }
