import os
from observability_client import ManagedMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def query_metric_window(metric_name: str, start_time: str, end_time: str) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring.
    """
    client = ManagedMetricsClient()
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        # project is loaded from config in the client
    )
    response = client.query_metric_window(request)
    return response
