# [SAME-SCENARIO] query_metric_window.py

from observability_client import CloudWatchClient
from observability_models import MetricQueryRequest, MetricQueryResponse


def query_metric_window(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 60) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window using Amazon CloudWatch Metrics.
    """
    client = CloudWatchClient()
    request = MetricQueryRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=['Average', 'Sum']
    )
    response = client.get_metric_data(request)
    return response
