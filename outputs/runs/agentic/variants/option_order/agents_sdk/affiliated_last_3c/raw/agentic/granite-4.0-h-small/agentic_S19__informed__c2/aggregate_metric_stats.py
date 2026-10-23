# [SAME-SCENARIO] aggregate_metric_stats.py

from observability_client import CloudWatchClient
from observability_models import MetricStatRequest, MetricStatResponse


def aggregate_metric_stats(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 300, statistics: list = ['Average', 'Sum', 'Maximum', 'Minimum']) -> MetricStatResponse:
    """Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch Metrics.
    """
    client = CloudWatchClient()
    request = MetricStatRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=statistics
    )
    response = client.get_metric_statistics(request)
    return response
