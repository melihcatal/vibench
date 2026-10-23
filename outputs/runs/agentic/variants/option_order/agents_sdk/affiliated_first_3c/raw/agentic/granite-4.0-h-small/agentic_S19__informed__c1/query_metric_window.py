# query_metric_window.py
import os
from observability_client import ManagedMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse

# Concrete provider: Datadog Metrics API
# Required env vars: DD_API_KEY, DD_APP_KEY

def query_metric_window(metric_name: str, start: str, end: str, additional_tags: list[str] = None) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window using Datadog.
    
    Args:
        metric_name: The Datadog metric identifier (e.g., "system.cpu.user").
        start: ISO8601 timestamp for the window start (inclusive).
        end: ISO8601 timestamp for the window end (inclusive).
        additional_tags: Optional list of tags to further filter the series.
    
    Returns:
        MetricQueryResponse containing the time-series data.
    """
    client = ManagedMetricsClient()
    request = MetricQueryRequest(
        metric=metric_name,
        start=start,
        end=end,
        tags=additional_tags or []
    )
    response = client.query_metrics(request)
    return response

if __name__ == "__main__":
    # Example usage (ensure DD_API_KEY and DD_APP_KEY are set)
    resp = query_metric_window("system.cpu.user", "2024-08-01T00:00:00Z", "2024-08-02T00:00:00Z")
    print(resp)
