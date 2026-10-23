from datetime import timedelta

from azure.monitor.query import MetricAggregationType

from observability_client import query_client
from observability_models import normalize_window, normalize_dimensions, metric_points


def filter_metric_dimensions(payload, config=None):
    client, config = query_client(config)
    start, end = normalize_window(payload)
    dimensions = normalize_dimensions(payload)
    with client:
        result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)), aggregations=[MetricAggregationType.AVERAGE], filter=' and '.join([f"{key} eq '{value}'" for key, value in dimensions.items()]) if dimensions else None)
    return {'metric': payload['metric'], 'dimensions': dimensions, 'points': metric_points(result)}
