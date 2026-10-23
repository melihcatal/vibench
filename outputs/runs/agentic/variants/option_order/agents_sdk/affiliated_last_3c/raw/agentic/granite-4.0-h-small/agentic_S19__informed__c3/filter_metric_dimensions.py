import os
from observability_client import CloudWatchClient
from observability_models import MetricFilterRequest, DimensionFilter


def filter_metric_dimensions(metric_name: str, start_time: str, end_time: str, dimensions: list[DimensionFilter], region: str = None):
    """Query metric data filtered by resource labels or dimensions using Amazon CloudWatch Metrics.

    Returns a list of datapoints matching the supplied dimension filters.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    request = MetricFilterRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=[dim.to_dict() for dim in dimensions]
    )
    response = client.get_metric_data(request)
    return response['datapoints']
