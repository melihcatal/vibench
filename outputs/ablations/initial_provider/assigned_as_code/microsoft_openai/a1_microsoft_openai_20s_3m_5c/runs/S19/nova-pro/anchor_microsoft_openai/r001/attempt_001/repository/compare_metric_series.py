from azure.monitor.query import MetricsQueryClient, MetricAggregationType
from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from observability_client import get_metrics_client, format_timespan
from observability_models import MetricQueryRequest, MetricQueryResponse

def compare_metric_series(payload, config=None):
    config = config or {}
    start, end = format_timespan(payload['start_time'], payload['end_time'])
    client = get_metrics_client()
    result1 = client.query_resource(config['resource_id'], metric_names=[payload['metric1']],
                                   timespan=(start, end),
                                   granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                   aggregations=[MetricAggregationType.AVERAGE],
                                   filter=payload.get('filter1'))
    result2 = client.query_resource(config['resource_id'], metric_names=[payload['metric2']],
                                   timespan=(start, end),
                                   granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                   aggregations=[MetricAggregationType.AVERAGE],
                                   filter=payload.get('filter2'))
    points1 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in result1.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    points2 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
               for metric in result2.metrics for series in metric.timeseries
               for point in series.data if point.average is not None]
    return {'points1': sorted(points1, key=lambda point: point['timestamp']),
            'points2': sorted(points2, key=lambda point: point['timestamp'])}