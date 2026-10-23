from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def summarize_metric_trends(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[MetricAggregationType.AVERAGE])
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
              for metric in result.metrics for series in metric.timeseries
              for point in series.data if point.average is not None]
    if len(points) < 2:
        return {'trend': 'insufficient data'}
    last_point = points[-1]
    second_last_point = points[-2]
    if last_point['value'] > second_last_point['value']:
        return {'trend': 'increasing'}
    elif last_point['value'] < second_last_point['value']:
        return {'trend': 'decreasing'}
    else:
        return {'trend': 'stable'}