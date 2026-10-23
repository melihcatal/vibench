from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from observability_models import normalize_window, summarize_points


def metric_summary(payload, config=None):
    config = config or {}
    start, end = normalize_window(payload)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MAXIMUM, MetricAggregationType.MINIMUM])
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average if point.average is not None else point.maximum if point.maximum is not None else point.minimum)} for metric in result.metrics for series in metric.timeseries for point in series.data if any(value is not None for value in (point.average, point.maximum, point.minimum))]
    stats = summarize_points(points)
    trend = 'stable'
    if stats['count'] > 1 and points[-1]['value'] > points[0]['value']:
        trend = 'rising'
    elif stats['count'] > 1 and points[-1]['value'] < points[0]['value']:
        trend = 'falling'
    return {'metric': payload['metric'], 'trend': trend, 'stats': stats, 'points': points}
