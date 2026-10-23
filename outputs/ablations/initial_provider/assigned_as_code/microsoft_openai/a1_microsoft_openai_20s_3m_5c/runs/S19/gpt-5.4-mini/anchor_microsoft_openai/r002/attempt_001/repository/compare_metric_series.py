from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from observability_client import load_config


def _series_points(client, resource_id, metric_name, start, end, period_seconds, dimension_filter=None):
    kwargs = {'metric_names': [metric_name], 'timespan': (start, end), 'granularity': timedelta(seconds=period_seconds), 'aggregations': [MetricAggregationType.AVERAGE]}
    if dimension_filter:
        kwargs['filter'] = dimension_filter
    result = client.query_resource(resource_id, **kwargs)
    return [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)} for metric in result.metrics for series in metric.timeseries for point in series.data if point.average is not None]


def compare_metric_series(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            left = _series_points(client, config['resource_id'], payload['metric'], start, end, config.get('period_seconds', 60), payload.get('left_filter'))
            right = _series_points(client, config['resource_id'], payload['metric'], start, end, config.get('period_seconds', 60), payload.get('right_filter'))
    return {'left': sorted(left, key=lambda point: point['timestamp']), 'right': sorted(right, key=lambda point: point['timestamp'])}
