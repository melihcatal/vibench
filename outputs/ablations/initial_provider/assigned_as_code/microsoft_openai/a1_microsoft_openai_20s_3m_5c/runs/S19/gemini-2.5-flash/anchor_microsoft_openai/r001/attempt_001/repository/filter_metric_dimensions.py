from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    
    # The filter string format depends on the Azure Monitor metric dimensions
    # Example: "DimensionName eq 'DimensionValue'"
    # Assuming payload['dimension_filter'] is a dictionary like {'dimension_name': 'dimension_value'}
    filters = []
    for dim_name, dim_value in payload.get('dimension_filters', {}).items():
        filters.append(f"{dim_name} eq '{dim_value}'")
    
    filter_str = " and ".join(filters)

    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[MetricAggregationType.AVERAGE],
                filter=filter_str if filter_str else None)
    
    points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
              for metric in result.metrics for series in metric.timeseries
              for point in series.data if point.average is not None]
    return {'points': sorted(points, key=lambda point: point['timestamp'])}
