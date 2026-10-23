from datetime import datetime, timezone

from azure.monitor.query import MetricAggregationType

from observability_client import load_observability_config, metric_client, period_to_timedelta
from observability_models import normalize_points


def metric_summary(payload, config=None):
    config = load_observability_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with metric_client() as client:
        result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
            timespan=(start, end), granularity=period_to_timedelta(config),
            aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MAXIMUM, MetricAggregationType.MINIMUM])
    points = normalize_points(result)
    values = [point['value'] for point in points]
    return {'metric': payload['metric'], 'count': len(values), 'min': min(values) if values else None,
            'max': max(values) if values else None, 'latest': values[-1] if values else None, 'points': points}
