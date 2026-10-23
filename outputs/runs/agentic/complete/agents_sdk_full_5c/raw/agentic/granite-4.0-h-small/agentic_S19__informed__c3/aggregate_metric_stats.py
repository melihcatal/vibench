# [SAME-SCENARIO] aggregate_metric_stats.py
import os
from datetime import datetime, timedelta
from observability_client import Boto3Client
from observability_models import MetricRequest, MetricAggregateResponse

def aggregate_metric_stats(metric_name: str, namespace: str = None, dimensions: dict = None, window_hours: int = 2, statistic: str = "Average"):
    """Retrieve aggregated statistics (e.g., average, sum, max) for a metric over a time window using CloudWatch.
    Args:
        metric_name: The name of the metric.
        namespace: CloudWatch namespace (e.g., "AWS/EC2"). If None, defaults to "AWS/EC2".
        dimensions: Optional dict of dimension key/value pairs.
        window_hours: Lookback window in hours.
        statistic: Aggregation method ("Average", "Sum", "Maximum", "Minimum").
    Returns:
        A MetricAggregateResponse with the computed statistic.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)
    request = MetricRequest(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=dimensions,
        start_time=start_time.isoformat() + 'Z',
        end_time=end_time.isoformat() + 'Z',
        period=300,  # 5 minutes
        statistic=statistic
    )
    client = Boto3Client(service="cloudwatch")
    response = client.get_metric_statistics(request)
    return response

if __name__ == "__main__":
    # Example usage with environment variables for credentials
    print(aggregate_metric_stats("CPUUtilization", statistic="Sum"))
