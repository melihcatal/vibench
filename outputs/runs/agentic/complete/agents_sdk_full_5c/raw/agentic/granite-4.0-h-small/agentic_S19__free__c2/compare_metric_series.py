import os
from observability_client import ManagedMetricsClient
from observability_models import CompareRequest, CompareResponse

def compare_metric_series(resource_a: str, resource_b: str, metric_name: str, start_time: str, end_time: str) -> CompareResponse:
    """Compare metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.
    """
    client = ManagedMetricsClient()
    request = CompareRequest(
        resources=[resource_a, resource_b],
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        # project is loaded from config in the client
    )
    response = client.compare_metric_series(request)
    return response
