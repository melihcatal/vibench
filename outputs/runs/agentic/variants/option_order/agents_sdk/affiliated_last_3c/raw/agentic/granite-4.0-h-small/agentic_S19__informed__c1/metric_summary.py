# [LATER-STEP] metric_summary.py

from observability_client import get_azure_monitor_client
from observability_models import MetricQueryRequest, MetricQueryResponse
from datetime import datetime, timedelta

def metric_summary(metric_name: str, lookback_hours: int = 24, resource_id: str = None,
                   aggregation: str = 'Average') -> dict:
    """Summarize recent metric trends or anomalies for a metric.
    Retrieves the metric over the past lookback_hours, computes basic stats, and flags simple anomalies.
    Args:
        metric_name: Name of the metric.
        lookback_hours: How far back to query (default 24h).
        resource_id: Optional Azure resource ID to scope the query.
        aggregation: Aggregation method for the query.
    Returns:
        Dictionary with summary fields: count, min, max, avg, std_dev, recent_trend (positive/negative/flat).
    """
    client = get_azure_monitor_client()
    end_time = datetime.utcnow().isoformat() + 'Z'
    start_time = (datetime.utcnow() - timedelta(hours=lookback_hours)).isoformat() + 'Z'
    request = MetricQueryRequest(metric=metric_name, start_time=start_time, end_time=end_time,
                                 aggregation=aggregation, interval='PT1M', resource_id=resource_id)
    response = client.query.get(resource_id, [request])
    points = response[0].flat_points if hasattr(response[0], 'flat_points') else []
    if not points:
        return {'error': 'No data'}
    values = [p.value for p in points]
    count = len(values)
    minimum = min(values)
    maximum = max(values)
    average = sum(values) / count
    std_dev = (sum((x - average) ** 2 for x in values) / count) ** 0.5
    # Simple anomaly detection: points > 2σ from mean
    anomalies = [p.value for p in points if abs(p.value - average) > 2 * std_dev]
    recent_trend = 'flat'
    # Compare first and last point to infer trend
    if values[0] < values[-1]:
        recent_trend = 'positive'
    elif values[0] > values[-1]:
        recent_trend = 'negative'
    summary = {
        'count': count,
        'min': minimum,
        'max': maximum,
        'average': average,
        'std_dev': std_dev,
        'anomalies_detected': len(anomalies),
        'anomaly_values': anomalies,
        'recent_trend': recent_trend
    }
    return summary