import os
from observability_client import CloudWatchClient
from observability_models import MetricAggregateRequest, MetricStat


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str, period: int = 300, region: str = None):
    """Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch Metrics.

    Returns a dictionary with statistic names as keys and their computed values.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    request = MetricAggregateRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=['Average', 'Sum', 'Maximum', 'Minimum', 'SampleCount']
    )
    response = client.get_metric_statistics(request)
    return {
        stat: value for stat, value in zip(request.statistics, response['values'])
    }
