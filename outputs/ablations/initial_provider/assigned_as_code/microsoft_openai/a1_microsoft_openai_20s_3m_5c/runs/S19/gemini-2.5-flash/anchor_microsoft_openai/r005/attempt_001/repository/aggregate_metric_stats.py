from datetime import datetime, timedelta, timezone
from observability_client import AzureMonitorClient
from azure.monitor.query import MetricAggregationType


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    client = AzureMonitorClient().get_metrics_query_client()

    aggregations = [MetricAggregationType.from_str(agg.upper()) for agg in payload.get('aggregations', ['average'])]

    result = client.query_resource(
        config['resource_id'],
        metric_names=[payload['metric']],
        timespan=(start, end),
        granularity=timedelta(seconds=config.get('period_seconds', 60)),
        aggregations=aggregations
    )

    aggregated_data = {}
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                for agg_type in aggregations:
                    agg_value = getattr(point, agg_type.value.lower(), None)
                    if agg_value is not None:
                        if agg_type.value not in aggregated_data:
                            aggregated_data[agg_type.value] = []
                        aggregated_data[agg_type.value].append({
                            'timestamp': point.timestamp.timestamp(),
                            'value': float(agg_value)
                        })
    
    for agg_type in aggregated_data:
        aggregated_data[agg_type] = sorted(aggregated_data[agg_type], key=lambda p: p['timestamp'])

    return aggregated_data
