# [SAME-SCENARIO] filter_metric_dimensions.py

from observability_client import get_azure_monitor_client
from observability_models import MetricQueryRequest, MetricQueryResponse

def filter_metric_dimensions(metric_name: str, dimensions: dict, start_time: str, end_time: str,
                             resource_id: str = None) -> MetricQueryResponse:
    """Query metric data filtered by resource labels or dimensions using Azure Monitor Metrics.
    Args:
        metric_name: Name of the metric.
        dimensions: Dictionary of dimension name/value pairs (e.g., {'Environment': 'prod'}).
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.
        resource_id: Optional Azure resource ID.
    Returns:
        MetricQueryResponse containing filtered data points.
    """
    client = get_azure_monitor_client()
    query = MetricQueryRequest(metric=metric_name,
                               filter=' and '.join([f"{k} eq '{v}'" for k, v in dimensions.items()]),
                               start_time=start_time, end_time=end_time,
                               aggregation='Average', interval='PT1M', resource_id=resource_id)
    response = client.query.get(resource_id, [query])
    return response