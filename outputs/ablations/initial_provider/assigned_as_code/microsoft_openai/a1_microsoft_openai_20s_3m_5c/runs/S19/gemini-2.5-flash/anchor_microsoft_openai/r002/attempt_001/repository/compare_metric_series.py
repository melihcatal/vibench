from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def compare_metric_series(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)

    series_data = {}

    for i, filter_key in enumerate(['filter_a', 'filter_b']):
        filter_str = payload.get(filter_key)
        if not filter_str:
            continue

        with DefaultAzureCredential() as credential:
            with MetricsQueryClient(credential) as client:
                result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                                               timespan=(start, end),
                                               granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                               filter=filter_str,
                                               aggregations=[MetricAggregationType.AVERAGE])
        
        points = []
        for metric in result.metrics:
            for series in metric.timeseries:
                for point in series.data:
                    if point.average is not None:
                        points.append({'timestamp': point.timestamp.timestamp(), 'value': float(point.average)})
        series_data[filter_key] = sorted(points, key=lambda point: point['timestamp'])

    return series_data
