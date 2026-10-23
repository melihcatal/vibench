from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType

from observability_client import load_config, create_metrics_client
from observability_models import normalize_points


def compare_metric_series(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    credential, client = create_metrics_client()
    with credential:
        with client:
            result = client.query_resource(
                config['resource_id'],
                metric_names=[payload['metric']],
                timespan=(start, end),
                granularity=timedelta(seconds=config['period_seconds']),
                aggregations=[MetricAggregationType.AVERAGE],
            )
    series_map = {'left': [], 'right': []}
    filters = payload.get('filters', {})
    for metric in result.metrics:
        for series in metric.timeseries:
            dimensions = {item.name: item.value for item in getattr(series, 'metadatavalues', [])}
            for side in ('left', 'right'):
                criteria = filters.get(side, {})
                if all(dimensions.get(key) == value for key, value in criteria.items()):
                    for point in series.data:
                        if point.average is not None:
                            series_map[side].append({'timestamp': point.timestamp, 'value': float(point.average)})
    return {'metric': payload['metric'], 'left': normalize_points(series_map['left']), 'right': normalize_points(series_map['right'])}
