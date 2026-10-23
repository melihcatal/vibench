from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType
from observability_client import AzureObservabilityClient
from observability_models import MetricSeries, MetricPoint

def _query_series_data(client, resource_id, metric_name, start_time, end_time, period_seconds, dimension_filter):
    filters = []
    for dim_name, dim_value in dimension_filter.items():
        filters.append(f"{dim_name} eq '{dim_value}'")
    filter_expression = " and ".join(filters) if filters else None

    result = client.query_resource(
        resource_uri=resource_id,
        metric_names=[metric_name],
        timespan=(start_time, end_time),
        granularity=timedelta(seconds=period_seconds),
        aggregations=[MetricAggregationType.AVERAGE],
        filter=filter_expression
    )

    all_timeseries = []
    for metric in result.metrics:
        for series in metric.timeseries:
            points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
                      for point in series.data if point.average is not None]
            dimensions = {k: v for k, v in series.metadata.items() if k not in ["MetricName", "Aggregation"]}
            all_timeseries.append(MetricSeries(
                name=series.name,
                points=sorted(points, key=lambda p: p['timestamp']),
                dimensions=dimensions
            ))
    return all_timeseries

def compare_metric_series(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    period_seconds = config.get('period_seconds', 60)

    resource_id_1 = payload['series_1']['resource_id']
    metric_1 = payload['series_1']['metric']
    dimension_filters_1 = payload['series_1'].get('dimension_filters', {})

    resource_id_2 = payload['series_2']['resource_id']
    metric_2 = payload['series_2']['metric']
    dimension_filters_2 = payload['series_2'].get('dimension_filters', {})

    with AzureObservabilityClient() as client:
        series_data_1 = _query_series_data(client, resource_id_1, metric_1, start, end, period_seconds, dimension_filters_1)
        series_data_2 = _query_series_data(client, resource_id_2, metric_2, start, end, period_seconds, dimension_filters_2)

    return {
        'series_1_data': [s.__dict__ for s in series_data_1],
        'series_2_data': [s.__dict__ for s in series_data_2],
    }
