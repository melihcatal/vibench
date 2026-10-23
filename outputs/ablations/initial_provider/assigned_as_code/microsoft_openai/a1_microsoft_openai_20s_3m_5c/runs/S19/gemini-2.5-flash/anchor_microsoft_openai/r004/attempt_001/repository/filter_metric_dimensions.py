from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType
from observability_client import AzureObservabilityClient
from observability_models import MetricSeries, MetricPoint, MetricQueryResult

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)

    # Azure Monitor uses 'filter' for dimension-based filtering
    # The payload expects 'dimension_filters' as a dict, e.g., {'dimension_name': 'dimension_value'}
    filters = []
    for dim_name, dim_value in payload.get('dimension_filters', {}).items():
        filters.append(f"{dim_name} eq '{dim_value}'")
    filter_expression = " and ".join(filters) if filters else None

    with AzureObservabilityClient() as client:
        result = client.query_resource(
            resource_uri=config['resource_id'],
            metric_names=[payload['metric']],
            timespan=(start, end),
            granularity=timedelta(seconds=config.get('period_seconds', 60)),
            aggregations=[MetricAggregationType.AVERAGE], # Assuming average for filtered data display
            filter=filter_expression, # Apply dimension filter here
            # Azure Monitor does not directly support 'group by' in this client for all dimensions easily
            # For grouping, 'result_type=ResultType.DATA' and then manual processing or more advanced queries might be needed.
            # For this task, we assume simple filtering as per 'filter_metric_dimensions'.
        )

    all_timeseries = []
    for metric in result.metrics:
        for series in metric.timeseries:
            points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
                      for point in series.data if point.average is not None]
            # Extract dimensions from the series key-value pairs if available
            dimensions = {k: v for k, v in series.metadata.items() if k not in ["MetricName", "Aggregation"]}
            all_timeseries.append(MetricSeries(
                name=series.name,
                points=sorted(points, key=lambda p: p['timestamp']),
                dimensions=dimensions
            ))

    return {'metric_data': all_timeseries}
