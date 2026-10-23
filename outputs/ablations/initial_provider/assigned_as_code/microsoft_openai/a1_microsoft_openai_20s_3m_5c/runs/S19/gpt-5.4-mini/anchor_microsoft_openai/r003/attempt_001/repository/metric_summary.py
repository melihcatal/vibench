from azure.monitor.query import MetricAggregationType

from observability_client import get_client, get_config, get_credential, to_datetime
from observability_models import extract_points


def metric_summary(payload, config=None):
    config = get_config(config)
    start = to_datetime(payload['start_time'])
    end = to_datetime(payload['end_time'])
    with get_credential() as credential:
        with get_client(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=None, aggregations=[MetricAggregationType.AVERAGE])
    points = extract_points(result, 'average')
    values = [point['value'] for point in points]
    return {'count': len(values), 'minimum': min(values) if values else None, 'maximum': max(values) if values else None, 'average': (sum(values) / len(values)) if values else None}
