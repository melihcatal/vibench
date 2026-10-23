from datetime import datetime, timedelta, timezone
from observability_client import AzureMonitorClient
from azure.monitor.query import MetricAggregationType


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    client = AzureMonitorClient().get_metrics_query_client()

    filters = []
    if 'dimensions' in payload:
        for dim_name, dim_value in payload['dimensions'].items():
            filters.append(f"{dim_name} eq '{dim_value}'")

    filter_str = " and ".join(filters) if filters else None

    result = client.query_resource(
        config['resource_id'],
        metric_names=[payload['metric']],
        timespan=(start, end),
        granularity=timedelta(seconds=config.get('period_seconds', 60)),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=filter_str
    )

    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average),
               'dimensions': series.metadata}
              for metric in result.metrics for series in metric.timeseries
              for point in series.data if point.average is not None]

    return {'points': sorted(points, key=lambda point: point['timestamp'])}
