from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from observability_client import load_config


def filter_metric_dimensions(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    dimension_name = payload['dimension_name']
    dimension_value = payload['dimension_value']
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)), aggregations=[MetricAggregationType.AVERAGE], filter=f"{dimension_name} eq '{dimension_value}'")
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)} for metric in result.metrics for series in metric.timeseries for point in series.data if point.average is not None]
    return {'points': sorted(points, key=lambda point: point['timestamp'])}
