from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient


def compare_metric_series(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result1 = client.query_resource(config['resource_id'], metric_names=[payload['metric1']],
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[MetricAggregationType.AVERAGE])
            result2 = client.query_resource(config['resource_id'], metric_names=[payload['metric2']],
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[MetricAggregationType.AVERAGE])
    series1 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in result1.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    series2 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in result2.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    return {'series1': sorted(series1, key=lambda point: point['timestamp']),
            'series2': sorted(series2, key=lambda point: point['timestamp'])}