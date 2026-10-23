# [SAME-SCENARIO] aggregate_metric_stats.py

from observability_client import CloudWatchClient
from observability_models import MetricStatsRequest, MetricStatsResponse

def aggregate_metric_stats(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 300) -> MetricStatsResponse:
    """Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch.

    Args:
        namespace (str): CloudWatch namespace (e.g., "AWS/EC2").
        metric_name (str): Name of the metric.
        start_time (str): ISO8601 start time (e.g., "2025-08-15T10:00:00Z").
        end_time (str): ISO8601 end time (e.g., "2025-08-15T11:00:00Z").
        period (int): Granularity in seconds (default 300).

    Returns:
        MetricStatsResponse: Normalized response containing aggregated data (e.g., Sum, Avg, Min, Max).
    """
    client = CloudWatchClient()
    request = MetricStatsRequest(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Sum", "Average", "Minimum", "Maximum"]
    )
    response = client.get_metric_statistics(request)
    return response