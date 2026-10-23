from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[MetricAggregationType.MIN, MetricAggregationType.MAX, MetricAggregationType.TOTAL])
    stats = {
        'min': float(result.metrics[0].timeseries[0].data[0].minimum),
        'max': float(result.metrics[0].timeseries[0].data[0].maximum),
        'total': float(result.metrics[0].timeseries[0].data[0].total)
    }
    return stats