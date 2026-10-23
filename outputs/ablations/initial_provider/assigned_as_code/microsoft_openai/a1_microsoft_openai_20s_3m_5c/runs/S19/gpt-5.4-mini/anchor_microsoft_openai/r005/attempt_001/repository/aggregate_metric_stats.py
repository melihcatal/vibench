from datetime import datetime, timedelta, timezone
from azure.monitor.query import MetricAggregationType

from observability_client import load_config, create_metrics_client
from observability_models import summarize_values


def aggregate_metric_stats(payload, config=None):
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
                aggregations=[MetricAggregationType.AVERAGE, MetricAggregationType.MINIMUM, MetricAggregationType.MAXIMUM],
            )
    values = []
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                for attr in ('average', 'minimum', 'maximum'):
                    value = getattr(point, attr, None)
                    if value is not None:
                        values.append(float(value))
    summary = summarize_values(values)
    summary['metric'] = payload['metric']
    return summary
