from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from observability_client import load_config


def metric_summary(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)), aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM])
    values = [float(point.average) for metric in result.metrics for series in metric.timeseries for point in series.data if point.average is not None]
    if not values:
        return {'trend': 'unknown', 'anomaly': False}
    return {'trend': 'rising' if values[-1] >= values[0] else 'falling', 'anomaly': (max(values) - min(values)) > (sum(values) / len(values))}
