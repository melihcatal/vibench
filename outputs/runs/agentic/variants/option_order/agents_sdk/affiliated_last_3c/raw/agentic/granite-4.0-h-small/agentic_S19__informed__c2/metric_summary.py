# [LATER-STEP] metric_summary.py

from observability_client import CloudWatchClient
from observability_models import MetricStatRequest, MetricStatResponse


def metric_summary(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 300) -> MetricStatResponse:
    """Summarize recent metric trends or anomalies using Amazon CloudWatch Metrics.
    This implementation retrieves average, sum, max, and min values.
    """
    client = CloudWatchClient()
    request = MetricStatRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=['Average', 'Sum', 'Maximum', 'Minimum']
    )
    response = client.get_metric_statistics(request)
    return response
