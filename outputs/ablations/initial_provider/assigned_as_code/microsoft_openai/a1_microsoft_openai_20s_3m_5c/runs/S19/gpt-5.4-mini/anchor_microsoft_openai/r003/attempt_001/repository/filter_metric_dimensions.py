from azure.monitor.query import MetricAggregationType

from observability_client import get_client, get_config, get_credential, to_datetime
from observability_models import extract_series


def filter_metric_dimensions(payload, config=None):
    config = get_config(config)
    start = to_datetime(payload['start_time'])
    end = to_datetime(payload['end_time'])
    filters = payload.get('dimensions') or {}
    dimension_filter = ",".join(f"{key} eq '{value}'" for key, value in filters.items()) if filters else None
    with get_credential() as credential:
        with get_client(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=None, aggregations=[MetricAggregationType.AVERAGE], filter=dimension_filter)
    return {'series': extract_series(result, 'average')}
