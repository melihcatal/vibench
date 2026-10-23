from datetime import datetime, timedelta, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    start = datetime.fromtimestamp(payload['start_time'], tz=timezone.utc)
    end = datetime.fromtimestamp(payload['end_time'], tz=timezone.utc)
    with DefaultAzureCredential() as credential:
        with MetricsQueryClient(credential) as client:
            result = client.query_resource(config['resource_id'], metric_names=[payload['metric']],
                                           timespan=(start, end),
                                           granularity=timedelta(seconds=config.get('period_seconds', 60)),
                                           aggregations=[MetricAggregationType.MIN, MetricAggregationType.MAX,
                                                         MetricAggregationType.AVERAGE, MetricAggregationType.COUNT,
                                                         MetricAggregationType.TOTAL])
    
    stats = {}
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                if point.average is not None:
                    stats.setdefault('average', []).append(float(point.average))
                if point.minimum is not None:
                    stats.setdefault('minimum', []).append(float(point.minimum))
                if point.maximum is not None:
                    stats.setdefault('maximum', []).append(float(point.maximum))
                if point.count is not None:
                    stats.setdefault('count', []).append(float(point.count))
                if point.total is not None:
                    stats.setdefault('total', []).append(float(point.total))

    return {k: sum(v) / len(v) if v else None for k, v in stats.items()}
