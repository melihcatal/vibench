# [SAME-SCENARIO] compare_metric_series.py

from observability_client import get_azure_monitor_client
from observability_models import MetricQueryRequest, MetricQueryResponse

def compare_metric_series(metric_name: str, dimension_filter_a: dict, dimension_filter_b: dict,
                          start_time: str, end_time: str, resource_id: str = None) -> tuple[MetricQueryResponse, MetricQueryResponse]:
    """Compare metric values for two resources or dimension filters over the same window.
    Args:
        metric_name: Metric name.
        dimension_filter_a: Filter dict for first series (e.g., {'resource': 'a1'}).
        dimension_filter_b: Filter dict for second series (e.g., {'resource': 'b2'}).
        start_time, end_time: Time window.
        resource_id: Optional common Azure resource ID; filters will override if needed.
    Returns:
        Tuple of MetricQueryResponse for the two series.
    """
    client = get_azure_monitor_client()
    query_a = MetricQueryRequest(metric=metric_name,
                                 filter=' and '.join([f"{k} eq '{v}'" for k, v in dimension_filter_a.items()]),
                                 start_time=start_time, end_time=end_time,
                                 aggregation='Average', interval='PT1M', resource_id=resource_id)
    query_b = MetricQueryRequest(metric=metric_name,
                                 filter=' and '.join([f"{k} eq '{v}'" for k, v in dimension_filter_b.items()]),
                                 start_time=start_time, end_time=end_time,
                                 aggregation='Average', interval='PT1M', resource_id=resource_id)
    response_a = client.query.get(resource_id, [query_a])
    response_b = client.query.get(resource_id, [query_b])
    return response_a, response_b