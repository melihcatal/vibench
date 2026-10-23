from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from observability_client import get_metrics_client, format_timespan
from observability_models import MetricQueryRequest, MetricQueryResponse

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    start, end = format_timespan(payload['start_time'], payload['end_time'])
    client = get_metrics_client()
    result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                                   timespan=(start, end),
                                   granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                   aggregations=[MetricAggregationType.AVERAGE],
                                   filter=payload.get('filter'))
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in result.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    return {'points': sorted(points, key=lambda point: point['timestamp'])}