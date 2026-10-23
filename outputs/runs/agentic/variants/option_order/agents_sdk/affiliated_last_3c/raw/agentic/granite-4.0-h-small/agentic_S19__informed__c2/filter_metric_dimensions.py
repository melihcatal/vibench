# [SAME-SCENARIO] filter_metric_dimensions.py

from observability_client import CloudWatchClient
from observability_models import MetricFilterRequest, MetricFilterResponse


def filter_metric_dimensions(namespace: str, metric_name: str, start_time: str, end_time: str, resource_label: str, label_value: str, period: int = 60) -> MetricFilterResponse:
    """Query metric data filtered by a specific resource label or dimension using Amazon CloudWatch Metrics.
    """
    client = CloudWatchClient()
    request = MetricFilterRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=[{'Name': resource_label, 'Value': label_value}],
        period=period,
        statistics=['Average']
    )
    response = client.get_metric_data(request)
    return response
