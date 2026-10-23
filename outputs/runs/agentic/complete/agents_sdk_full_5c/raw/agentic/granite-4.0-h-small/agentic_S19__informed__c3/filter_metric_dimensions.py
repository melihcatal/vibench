# [SAME-SCENARIO] filter_metric_dimensions.py
import os
from datetime import datetime, timedelta
from observability_client import Boto3Client
from observability_models import MetricRequest, MetricResponse

def filter_metric_dimensions(metric_name: str, dimensions_filter: dict, namespace: str = None, window_hours: int = 2):
    """Query metric data filtered by specific dimension key/value pairs using CloudWatch.
    Args:
        metric_name: The name of the metric.
        dimensions_filter: Dictionary where keys are dimension names and values are exact values to filter on.
        namespace: CloudWatch namespace (e.g., "AWS/EC2"). If None, defaults to "AWS/EC2".
        window_hours: Lookback window in hours.
    Returns:
        A MetricResponse containing the filtered datapoints.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)
    request = MetricRequest(
        metric_name=metric_name,
        namespace=namespace,
        dimensions=dimensions_filter,
        start_time=start_time.isoformat() + 'Z',
        end_time=end_time.isoformat() + 'Z',
        period=300  # 5 minutes
    )
    client = Boto3Client(service="cloudwatch")
    response = client.get_metric_statistics(request)
    return response

if __name__ == "__main__":
    # Example: filter by instance ID
    print(filter_metric_dimensions("CPUUtilization", dimensions_filter={"InstanceId": ["i-0abcd1234ef567890"]}))
