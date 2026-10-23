# SAME-SCENARIO
import statistics
from observability_client import get_monitoring_client

def aggregate_metric_stats(metric_name, start_time, end_time):
    """Retrieve aggregated statistics for a metric over a time window.

    Args:
        metric_name (str): The metric identifier.
        start_time (str): RFC3339 timestamp for the window start.
        end_time (str): RFC3339 timestamp for the window end.

    Returns:
        dict: Aggregated statistics (count, sum, mean, min, max).
    """
    client = get_monitoring_client()
    response = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{metric_name}"',
            startTime=start_time,
            endTime=end_time,
            aggregation={'alignmentPeriod': '60s', 'perSeriesAligner': 'ALIGN_MEAN'}
        )
        .execute()
    # Compute simple aggregates from the returned points.
    points = []
    for series in response.get('timeSeries', []):
        for point in series.get('points', []):
            points.append(point.get('value', {}).get('doubleValue', 0))
    count = len(points)
    total = sum(points)
    mean = total / count if count else 0
    minimum = min(points) if points else None
    maximum = max(points) if points else None
    return {
        'count': count,
        'sum': total,
        'mean': mean,
        'min': minimum,
        'max': maximum
    }
