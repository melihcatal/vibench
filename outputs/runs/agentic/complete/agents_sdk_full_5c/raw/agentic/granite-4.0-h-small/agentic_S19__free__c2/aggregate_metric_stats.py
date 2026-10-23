import os
from observability_client import ManagedMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str) -> MetricQueryResponse:
    """Retrieve aggregated statistics for a metric over a time window using Google Cloud Monitoring.
    """
    client = ManagedMetricsClient()
    request = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation='SUM',
        # project is loaded from config in the client
    )
    response = client.aggregate_metric_stats(request)
    return response
