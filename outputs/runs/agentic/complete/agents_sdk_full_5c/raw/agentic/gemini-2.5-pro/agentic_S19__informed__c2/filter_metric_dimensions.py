from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id

def query_metric_with_filter(metric_type: str, dimension_key: str, dimension_value: str, minutes_ago: int = 10):
    """
    Queries metric data filtered by a specific resource dimension.
    
    Args:
        metric_type: The metric to query.
        dimension_key: The resource label key to filter on (e.g., "instance_name").
        dimension_value: The specific value of the label to match.
        minutes_ago: The time window in minutes.
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

    # Example filter: 'metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_name = "my-instance-1"'
    filter_str = f'metric.type = "{metric_type}" AND resource.labels.{dimension_key} = "{dimension_value}"'

    request = {
        "name": project_name,
        "filter": filter_str,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = client.list_time_series(request=request)
    return list(results)
