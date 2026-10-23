import os
from observability_client import CloudWatchClient
from observability_models import MetricQueryRequest, MetricWindow


def query_metric_window(metric_name: str, start_time: str, end_time: str, region: str = None):
    """Query recent datapoints for a named metric over a time window using Amazon CloudWatch Metrics.

    Returns a list of datapoints with timestamp and value.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=60,  # seconds
        statistics=['Average']
    )
    response = client.get_metric_data(request)
    return response['datapoints']
