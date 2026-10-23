from datetime import timedelta

from azure.monitor.query import MetricAggregationType

from observability_client import query_client
from observability_models import normalize_window, metric_points, summarize_points


def aggregate_metric_stats(payload, config=None):
    client, config = query_client(config)
    start, end = normalize_window(payload)
    with client:
        result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)), aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM, MetricAggregationType.TOTAL, MetricAggregationType.COUNT])
    points = metric_points(result)
    stats = summarize_points(points)
    return {'metric': payload['metric'], 'window': {'start_time': start.timestamp(), 'end_time': end.timestamp()}, 'stats': stats, 'points': points}
