# SAME-SCENARIO
from observability_client import get_monitoring_client

def query_metric_window(metric_name, start_time, end_time, limit=100):
    """Query recent datapoints for a named metric over a time window.

    Args:
        metric_name (str): The metric identifier.
        start_time (str): RFC3339 timestamp for the window start.
        end_time (str): RFC3339 timestamp for the window end.
        limit (int): Max number of points to return.

    Returns:
        List[dict]: Parsed metric datapoints.
    """
    client = get_monitoring_client()
    # Using Google Cloud Monitoring (Stackdriver) as the concrete provider.
    # The client wraps the Monitoring API endpoint.
    response = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{metric_name}"',
            startTime=start_time,
            endTime=end_time,
            pageSize=limit
        )
        .execute()
    # Normalize response to simple list of dicts.
    points = []
    for series in response.get('timeSeries', []):
        for point in series.get('points', []):
            points.append({
                'interval': point.get('interval'),
                'value': point.get('value')
            })
    return points
