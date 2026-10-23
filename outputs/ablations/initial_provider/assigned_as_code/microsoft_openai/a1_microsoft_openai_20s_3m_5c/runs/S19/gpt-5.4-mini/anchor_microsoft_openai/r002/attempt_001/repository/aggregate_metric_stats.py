from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from observability_client import load_config


def aggregate_metric_stats(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    aggregations = [MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM, MetricAggregationType.TOTAL, MetricAggregationType.COUNT]
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)), aggregations=aggregations)
    summary = {'average': None, 'minimum': None, 'maximum': None, 'total': None, 'count': None}
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                if point.average is not None:
                    summary['average'] = float(point.average)
                if point.minimum is not None:
                    summary['minimum'] = float(point.minimum)
                if point.maximum is not None:
                    summary['maximum'] = float(point.maximum)
                if point.total is not None:
                    summary['total'] = float(point.total)
                if point.count is not None:
                    summary['count'] = float(point.count)
    return summary
