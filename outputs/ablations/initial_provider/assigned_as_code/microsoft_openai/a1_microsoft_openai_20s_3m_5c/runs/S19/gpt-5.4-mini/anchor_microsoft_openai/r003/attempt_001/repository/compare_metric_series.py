from azure.monitor.query import MetricAggregationType

from observability_client import get_client, get_config, get_credential, to_datetime
from observability_models import extract_series


def compare_metric_series(payload, config=None):
    config = get_config(config)
    start = to_datetime(payload['start_time'])
    end = to_datetime(payload['end_time'])
    left_filter = payload['left_filter']
    right_filter = payload['right_filter']
    with get_credential() as credential:
        with get_client(credential) as client:
            left = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=None, aggregations=[MetricAggregationType.AVERAGE], filter=left_filter)
            right = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=None, aggregations=[MetricAggregationType.AVERAGE], filter=right_filter)
    return {'left': extract_series(left, 'average'), 'right': extract_series(right, 'average')}
