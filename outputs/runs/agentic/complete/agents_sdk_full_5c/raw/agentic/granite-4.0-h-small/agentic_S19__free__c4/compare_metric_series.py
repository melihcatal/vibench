# SAME-SCENARIO
from observability_client import get_monitoring_client

def compare_metric_series(metric_name, dimension_a, dimension_b, start_time, end_time, limit=100):
    """Compare metric values for two resources or dimension filters over the same window.

    Args:
        metric_name (str): The metric identifier.
        dimension_a (str): First dimension filter expression.
        dimension_b (str): Second dimension filter expression.
        start_time (str): RFC3339 timestamp for the window start.
        end_time (str): RFC3339 timestamp for the window end.
        limit (int): Max number of points to return.

    Returns:
        tuple: (series_a, series_b) where each is a list of (timestamp, value) pairs.
    """
    client = get_monitoring_client()
    series_a = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{metric_name}" AND {dimension_a}',
            startTime=start_time,
            endTime=end_time,
            pageSize=limit
        )
        .execute()
    series_b = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{metric_name}" AND {dimension_b}',
            startTime=start_time,
            endTime=end_time,
            pageSize=limit
        )
        .execute()
    def extract(series):
        result = []
        for s in series.get('timeSeries', []):
            for pt in s.get('points', []):
                result.append((pt.get('interval', {}).get('endTime'), pt.get('value')
                              .get('doubleValue')))
        return result
    return extract(series_a), extract(series_b)
