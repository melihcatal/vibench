import os
from observability_client import ManagedMetricsClient
from observability_models import MetricFilterRequest, MetricFilterResponse

def filter_metric_dimensions(metric_name: str, dimensions: dict, start_time: str, end_time: str) -> MetricFilterResponse:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring.
    """
    client = ManagedMetricsClient()
    request = MetricFilterRequest(
        metric_name=metric_name,
        dimensions=dimensions,
        start_time=start_time,
        end_time=end_time,
        # project is loaded from config in the client
    )
    response = client.filter_metric_dimensions(request)
    return response
