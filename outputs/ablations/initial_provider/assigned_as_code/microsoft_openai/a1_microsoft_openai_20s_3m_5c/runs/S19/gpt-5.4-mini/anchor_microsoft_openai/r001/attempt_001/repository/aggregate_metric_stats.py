from datetime import datetime, timezone

from azure.monitor.query import MetricAggregationType

from observability_client import load_observability_config, metric_client, period_to_timedelta
from observability_models import normalize_points, metric_window_response


def aggregate_metric_stats(payload, config=None):
    config = load_observability_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    aggregations = payload.get('aggregations') or [MetricAggregationType.AVERAGE, MetricAggregationType.TOTAL]
    with metric_client() as client:
        result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
            timespan=(start, end), granularity=period_to_timedelta(config), aggregations=aggregations)
    return metric_window_response(normalize_points(result), metric=payload['metric'], aggregations=[str(a) for a in aggregations])
