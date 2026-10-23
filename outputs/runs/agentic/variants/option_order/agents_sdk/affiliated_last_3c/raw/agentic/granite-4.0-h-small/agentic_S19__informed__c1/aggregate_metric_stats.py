# [SAME-SCENARIO] aggregate_metric_stats.py

from observability_client import get_azure_monitor_client
from observability_models import MetricStatisticsRequest, MetricStatisticsResponse

def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str, resource_id: str = None,
                           aggregation: str = 'Average') -> MetricStatisticsResponse:
    """Retrieve aggregated statistics for a metric over a time window using Azure Monitor Metrics.
    Args:
        metric_name: Name of the metric to query.
        start_time: ISO 8601 start time.
        end_time: ISO 8601 end time.
        resource_id: Optional Azure resource ID.
        aggregation: Aggregation method (e.g., 'Average', 'Sum', 'Max', 'Min').
    Returns:
        MetricStatisticsResponse with aggregated values.
    """
    client = get_azure_monitor_client()
    request = MetricStatisticsRequest(metric=metric_name, start_time=start_time, end_time=end_time,
                                      aggregation=aggregation, interval='PT1M', resource_id=resource_id)
    response = client.query.get(resource_id, [request])
    return response