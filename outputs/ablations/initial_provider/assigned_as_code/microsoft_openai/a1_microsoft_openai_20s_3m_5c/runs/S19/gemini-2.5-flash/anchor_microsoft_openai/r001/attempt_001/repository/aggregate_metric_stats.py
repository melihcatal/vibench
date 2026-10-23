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
                timespan=(start, end), granularity=timedelta(seconds=config.get('period_seconds', 60)),
                aggregations=[
                    MetricAggregationType.AVERAGE,
                    MetricAggregationType.MAXIMUM,
                    MetricAggregationType.MINIMUM,
                    MetricAggregationType.COUNT,
                    MetricAggregationType.TOTAL
                ])
    
    aggregated_data = {}
    for metric in result.metrics:
        for series in metric.timeseries:
            for point in series.data:
                # Assuming we want the overall aggregate for the window, not per-point aggregation
                # Azure Monitor SDK returns aggregated data per time grain, so we'll just take the last point's aggregate
                if point.average is not None:
                    aggregated_data['average'] = float(point.average)
                if point.maximum is not None:
                    aggregated_data['maximum'] = float(point.maximum)
                if point.minimum is not None:
                    aggregated_data['minimum'] = float(point.minimum)
                if point.count is not None:
                    aggregated_data['count'] = float(point.count)
                if point.total is not None:
                    aggregated_data['total'] = float(point.total)
    
    return {'aggregations': aggregated_data}
