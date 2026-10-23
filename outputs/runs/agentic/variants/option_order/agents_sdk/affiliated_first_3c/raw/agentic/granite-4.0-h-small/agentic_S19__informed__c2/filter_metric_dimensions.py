# [SAME-SCENARIO] filter_metric_dimensions.py

from observability_client import CloudWatchClient
from observability_models import MetricFilterRequest, MetricFilterResponse

def filter_metric_dimensions(namespace: str, metric_name: str, start_time: str, end_time: str, dimensions: dict) -> MetricFilterResponse:
    """Query metric data filtered by resource labels or dimensions using Amazon CloudWatch.

    Args:
        namespace (str): CloudWatch namespace.
        metric_name (str): Metric name.
        start_time (str): ISO8601 start time.
        end_time (str): ISO8601 end time.
        dimensions (dict): Filter dimensions (e.g., {"InstanceId": ["i-123abc"]}).

    Returns:
        MetricFilterResponse: Normalized response with datapoints matching the filters.
    """
    client = CloudWatchClient()
    request = MetricFilterRequest(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Dimensions=dimensions
    )
    response = client.get_metric_data(request)
    return response