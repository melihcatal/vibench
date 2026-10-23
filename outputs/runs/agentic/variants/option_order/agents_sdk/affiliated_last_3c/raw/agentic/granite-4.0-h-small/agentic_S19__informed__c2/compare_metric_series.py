# [SAME-SCENARIO] compare_metric_series.py

from observability_client import CloudWatchClient
from observability_models import MetricCompareRequest, MetricCompareResponse


def compare_metric_series(namespace: str, metric_name: str, resource1: str, resource2: str, start_time: str, end_time: str, period: int = 60) -> MetricCompareResponse:
    """Compare metric values for two resources (or dimension values) over the same time window using Amazon CloudWatch Metrics.
    """
    client = CloudWatchClient()
    request = MetricCompareRequest(
        namespace=namespace,
        metric_name=metric_name,
        dimensions=[
            {'Name': 'Resource', 'Value': resource1},
            {'Name': 'Resource', 'Value': resource2}
        ],
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=['Average']
    )
    response = client.get_metric_data(request)
    return response
