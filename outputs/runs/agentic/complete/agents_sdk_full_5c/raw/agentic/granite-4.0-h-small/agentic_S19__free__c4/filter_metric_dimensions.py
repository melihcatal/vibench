# SAME-SCENARIO
from observability_client import get_monitoring_client

def filter_metric_dimensions(metric_name, dimension_filter, start_time, end_time, limit=100):
    """Query metric data filtered by resource labels or dimensions.

    Args:
        metric_name (str): The metric identifier.
        dimension_filter (str): Dimension label filter expression (e.g., 'resource.label.env="prod").
        start_time (str): RFC3339 timestamp for the window start.
        end_time (str): RFC3339 timestamp for the window end.
        limit (int): Max number of points to return.

    Returns:
        List[dict]: Parsed metric datapoints that match the filter.
    """
    client = get_monitoring_client()
    filter_expr = f'metric.type="custom.googleapis.com/{metric_name}" AND {dimension_filter}'
    response = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=filter_expr,
            startTime=start_time,
            endTime=end_time,
            pageSize=limit
        )
        .execute()
    points = []
    for series in response.get('timeSeries', []):
        for point in series.get('points', []):
            points.append({
                'interval': point.get('interval'),
                'value': point.get('value')
            })
    return points
