from azure.monitor.query import MetricAggregationType

from observability_client import get_client, get_config, get_credential, to_datetime
from observability_models import extract_points


def aggregate_metric_stats(payload, config=None):
    config = get_config(config)
    start = to_datetime(payload['start_time'])
    end = to_datetime(payload['end_time'])
    aggregations = [MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM, MetricAggregationType.TOTAL, MetricAggregationType.COUNT]
    with get_credential() as credential:
        with get_client(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']], timespan=(start, end), granularity=None, aggregations=aggregations)
    return {'points': extract_points(result, 'average')}
