from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType

from observability_client import load_config, create_metrics_client
from observability_models import normalize_points


def filter_metric_dimensions(payload, config=None):
    config = load_config(config)
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    criteria = payload.get('dimensions', {})
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
    points = []
    for metric in result.metrics:
        for series in metric.timeseries:
            dimensions = {item.name: item.value for item in getattr(series, 'metadatavalues', [])}
            if all(dimensions.get(key) == value for key, value in criteria.items()):
                for point in series.data:
                    if point.average is not None:
                        points.append({'timestamp': point.timestamp, 'value': float(point.average), 'dimensions': dimensions})
    normalized = normalize_points(points)
    return {'metric': payload['metric'], 'points': normalized}
