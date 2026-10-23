from datetime import datetime, timedelta, timezone
from observability_client import AzureMonitorClient
from azure.monitor.query import MetricAggregationType


def compare_metric_series(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    client = AzureMonitorClient().get_metrics_query_client()

    results = {}

    # Query for series 1
    filter_str_1 = None
    if 'dimensions_1' in payload:
        filters = [f"{dim_name} eq '{dim_value}'" for dim_name, dim_value in payload['dimensions_1'].items()]
        filter_str_1 = " and ".join(filters)

    result_1 = client.query_resource(
        config['resource_id'],
        metric_names=[payload['metric']],
        timespan=(start, end),
        granularity=timedelta(seconds=config.get('period_seconds', 60)),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=filter_str_1
    )
    points_1 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
                for metric in result_1.metrics for series in metric.timeseries
                for point in series.data if point.average is not None]
    results['series_1'] = sorted(points_1, key=lambda point: point['timestamp'])

    # Query for series 2
    filter_str_2 = None
    if 'dimensions_2' in payload:
        filters = [f"{dim_name} eq '{dim_value}'" for dim_name, dim_value in payload['dimensions_2'].items()]
        filter_str_2 = " and ".join(filters)

    result_2 = client.query_resource(
        config['resource_id'],
        metric_names=[payload['metric']],
        timespan=(start, end),
        granularity=timedelta(seconds=config.get('period_seconds', 60)),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=filter_str_2
    )
    points_2 = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
                for metric in result_2.metrics for series in metric.timeseries
                for point in series.data if point.average is not None]
    results['series_2'] = sorted(points_2, key=lambda point: point['timestamp'])

    return results
