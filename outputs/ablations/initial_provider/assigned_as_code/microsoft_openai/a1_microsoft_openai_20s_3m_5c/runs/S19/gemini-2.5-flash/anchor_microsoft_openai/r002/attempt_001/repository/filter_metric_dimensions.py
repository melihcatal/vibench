from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    filter_str = payload.get('filter', None)

    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                                           timespan=(start, end),
                                           granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                           filter=filter_str,
                                           aggregations=[MetricAggregationType.AVERAGE])
    
    filtered_points = []
    for metric in result.metrics:
        for series in metric.timeseries:
            metadata = {dimension.name: dimension.value for dimension in series.metadata_values}
            for point in series.data:
                if point.average is not None:
                    filtered_points.append({
                        'timestamp': point.timestamp.timestamp(),
                        'value': float(point.average),
                        'dimensions': metadata
                    })
    return {'points': sorted(filtered_points, key=lambda point: point['timestamp'])}
