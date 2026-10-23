# LATER-STEP
import statistics
from observability_client import get_monitoring_client
from observability_models import StatResult, MetricRequest

def metric_summary(metric_name, start_time, end_time):
    """Summarize recent metric trends or anomalies.

    Uses recent datapoints to compute basic stats and detect spikes.
    """
    client = get_monitoring_client()
    # Pull raw datapoints (simplified query similar to query_metric_window)
    response = client.projects().timeSeries()
        .list(
            name='projects/PROJECT_ID',
            filter=f'metric.type="custom.googleapis.com/{metric_name}"',
            startTime=start_time,
            endTime=end_time,
            pageSize=200
        )
        .execute()
    points = []
    for series in response.get('timeSeries', []):
        for pt in series.get('points', []):
            points.append(pt.get('value', {}).get('doubleValue'))
    if not points:
        return {'error': 'No data found'}
    count = len(points)
    total = sum(points)
    mean = total / count
    stdev = statistics.stdev(points) if count > 1 else 0.0
    min_val = min(points)
    max_val = max(points)
    # Simple anomaly detection: points > mean + 2*std
    anomalies = [p for p in points if p > mean + 2 * stdev]
    return {
        'count': count,
        'sum': total,
        'mean': mean,
        'stdev': stdev,
        'min': min_val,
        'max': max_val,
        'anomalies_count': len(anomalies),
        'anomalies_sample': anomalies[:10]  # sample first few
    }
