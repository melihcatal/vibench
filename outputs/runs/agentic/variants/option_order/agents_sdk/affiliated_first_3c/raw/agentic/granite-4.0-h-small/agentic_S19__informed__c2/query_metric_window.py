# [SAME-SCENARIO] query_metric_window.py

from observability_client import CloudWatchClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def query_metric_window(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 60) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window using Amazon CloudWatch.

    Args:
        namespace (str): CloudWatch namespace (e.g., "AWS/EC2").
        metric_name (str): Name of the metric.
        start_time (str): ISO8601 start time (e.g., "2025-08-15T10:00:00Z").
        end_time (str): ISO8601 end time (e.g., "2025-08-15T11:00:00Z").
        period (int): Granularity in seconds (default 60).

    Returns:
        MetricQueryResponse: Normalized response containing datapoints.
    """
    client = CloudWatchClient()
    request = MetricQueryRequest(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["SampleCount", "Average"]
    )
    response = client.get_metric_data(request)
    return response