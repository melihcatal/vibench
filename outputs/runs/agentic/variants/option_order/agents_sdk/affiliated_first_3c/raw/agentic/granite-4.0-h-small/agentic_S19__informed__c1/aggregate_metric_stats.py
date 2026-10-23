# aggregate_metric_stats.py
import os
from observability_client import ManagedMetricsClient
from observability_models import MetricStatsRequest, MetricStatsResponse

# Concrete provider: Amazon CloudWatch Metrics
# Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

def aggregate_metric_stats(metric_name: str, namespace: str, dimensions: dict, 
                           start: str, end: str, period: int, statistics: list[str]) -> MetricStatsResponse:
    """Retrieve aggregated statistics for a metric over a time window using CloudWatch.
    
    Args:
        metric_name: The metric identifier within the namespace (e.g., "CPUUtilization").
        namespace: CloudWatch namespace (e.g., "AWS/EC2").
        dimensions: Dict of dimension key/value pairs (e.g., {"InstanceId": "i-123456"}).
        start: ISO8601 timestamp for the window start (inclusive).
        end: ISO8601 timestamp for the window end (inclusive).
        period: Granularity in seconds for aggregation.
        statistics: List of statistic names (e.g., ["Average", "Maximum"]).
    
    Returns:
        MetricStatsResponse with the computed statistics.
    """
    client = ManagedMetricsClient()
    request = MetricStatsRequest(
        namespace=namespace,
        metric_name=metric_name,
        dimensions=dimensions,
        start=start,
        end=end,
        period=period,
        statistics=statistics
    )
    response = client.get_metric_statistics(request)
    return response

if __name__ == "__main__":
    # Example usage (ensure AWS credentials are set)
    stats = aggregate_metric_stats(
        metric_name="CPUUtilization",
        namespace="AWS/EC2",
        dimensions={"InstanceId": "i-0abcd1234efgh5678"},
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z",
        period=300,
        statistics=["Average", "Maximum"]
    )
    print(stats)
