from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType
from observability_client import AzureObservabilityClient
from observability_models import MetricStats

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    
    # Azure Monitor supports multiple aggregations in one call
    aggregations = []
    if 'min' in payload['statistics']: aggregations.append(MetricAggregationType.MINIMUM)
    if 'max' in payload['statistics']: aggregations.append(MetricAggregationType.MAXIMUM)
    if 'avg' in payload['statistics']: aggregations.append(MetricAggregationType.AVERAGE)
    if 'sum' in payload['statistics']: aggregations.append(MetricAggregationType.TOTAL)
    if 'count' in payload['statistics']: aggregations.append(MetricAggregationType.COUNT)

    if not aggregations:
        return {'error': 'No valid statistics requested.'}

    with AzureObservabilityClient() as client:
        result = client.query_resource(
            resource_uri=config['resource_id'],
            metric_names=[payload['metric']],
            timespan=(start, end),
            granularity=timedelta(seconds=config.get('period_seconds', 60)),
            aggregations=aggregations
        )

    stats = MetricStats(min=None, max=None, avg=None, sum=None, count=None)

    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                if MetricAggregationType.MINIMUM in aggregations and point.minimum is not None: stats.min = point.minimum
                if MetricAggregationType.MAXIMUM in aggregations and point.maximum is not None: stats.max = point.maximum
                if MetricAggregationType.AVERAGE in aggregations and point.average is not None: stats.avg = point.average
                if MetricAggregationType.TOTAL in aggregations and point.total is not None: stats.sum = point.total
                if MetricAggregationType.COUNT in aggregations and point.count is not None: stats.count = point.count

    return {'statistics': stats.__dict__}
