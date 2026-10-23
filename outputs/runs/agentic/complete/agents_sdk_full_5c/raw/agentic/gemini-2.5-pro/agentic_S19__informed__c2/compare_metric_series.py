from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id

def compare_two_metric_series(metric_type: str, dimension_key: str, value1: str, value2: str, minutes_ago: int = 15):
    """
    Compares metric values for two resources by querying them separately over the same window.
    
    Args:
        metric_type: The metric to query.
        dimension_key: The dimension to distinguish resources (e.g., "instance_name").
        value1: The value for the first resource.
        value2: The value for the second resource.
        minutes_ago: The time window in minutes.

    Returns:
        A dictionary containing the time series for both resources.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = monitoring_v3.TimeInterval(
        {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(now.timestamp())},
        }
    )

    def fetch_series(val):
        filter_str = f'metric.type = "{metric_type}" AND resource.labels.{dimension_key} = "{val}"'
        request = {
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
        return list(client.list_time_series(request=request))

    series1 = fetch_series(value1)
    series2 = fetch_series(value2)
    
    return {
        value1: series1,
        value2: series2
    }
