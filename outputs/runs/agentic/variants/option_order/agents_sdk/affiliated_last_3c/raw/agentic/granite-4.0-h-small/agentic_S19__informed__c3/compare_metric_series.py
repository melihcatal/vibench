import os
from observability_client import CloudWatchClient
from observability_models import MetricCompareRequest, CompareMetric


def compare_metric_series(metric_name: str, start_time: str, end_time: str, resource_a: str, resource_b: str, region: str = None):
    """Compare metric values for two resources or dimension filters over the same window using Amazon CloudWatch Metrics.

    Returns a tuple of two lists: (datapoints_resource_a, datapoints_resource_b).
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    request = MetricCompareRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        resources=[resource_a, resource_b],
        period=60
    )
    response = client.get_metric_data(request)
    return response['series_a'], response['series_b']
