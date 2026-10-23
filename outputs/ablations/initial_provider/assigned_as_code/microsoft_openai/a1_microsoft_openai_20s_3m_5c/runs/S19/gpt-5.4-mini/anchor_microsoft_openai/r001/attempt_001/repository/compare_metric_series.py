from datetime import datetime, timezone

from azure.monitor.query import MetricAggregationType

from observability_client import load_observability_config, metric_client, period_to_timedelta
from observability_models import normalize_points, metric_window_response


def compare_metric_series(payload, config=None):
    config = load_observability_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    first_filter = payload['left_filter']
    second_filter = payload['right_filter']
    with metric_client() as client:
        left = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
            timespan=(start, end), granularity=period_to_timedelta(config),
            aggregations=[MetricAggregationType.AVERAGE], filter=first_filter)
        right = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
            timespan=(start, end), granularity=period_to_timedelta(config),
            aggregations=[MetricAggregationType.AVERAGE], filter=second_filter)
    return metric_window_response({'left': normalize_points(left), 'right': normalize_points(right)}, metric=payload['metric'])
