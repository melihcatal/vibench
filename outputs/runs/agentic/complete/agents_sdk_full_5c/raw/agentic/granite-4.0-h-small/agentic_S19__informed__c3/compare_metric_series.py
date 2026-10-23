# [SAME-SCENARIO] compare_metric_series.py
import os
from datetime import datetime, timedelta
from observability_client import Boto3Client
from observability_models import MetricRequest, MetricResponse

def compare_metric_series(metric_name: str, resource_a: str, resource_b: str, dimensions: dict = None, window_hours: int = 2):
    """Compare metric values for two resources (e.g., two EC2 instance IDs) over the same time window using CloudWatch.
    Args:
        metric_name: The name of the metric.
        resource_a, resource_b: Identifiers (e.g., InstanceId) of the two resources to compare.
        dimensions: Optional additional dimension filters.
        window_hours: Lookback window in hours.
    Returns:
        A tuple (response_a, response_b) with MetricResponse objects for each resource.
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=window_hours)
    base_req = MetricRequest(
        metric_name=metric_name,
        start_time=start_time.isoformat() + 'Z',
        end_time=end_time.isoformat() + 'Z',
        period=300,  # 5 minutes
    )
    client = Boto3Client(service="cloudwatch")
    # Query first resource – add its dimension to the request
    req_a = base_req.copy()
    req_a.dimensions = {**dimensions, "InstanceId": resource_a} if dimensions else {"InstanceId": resource_a}
    resp_a = client.get_metric_statistics(req_a)
    # Query second resource
    req_b = base_req.copy()
    req_b.dimensions = {**dimensions, "InstanceId": resource_b} if dimensions else {"InstanceId": resource_b}
    resp_b = client.get_metric_statistics(req_b)
    return resp_a, resp_b

if __name__ == "__main__":
    # Example comparing two specific EC2 instances
    a, b = compare_metric_series("CPUUtilization", "i-0abcd1234ef567890", "i-0xyz9876lmnopqrs")
    print("Resource A:", a)
    print("Resource B:", b)
