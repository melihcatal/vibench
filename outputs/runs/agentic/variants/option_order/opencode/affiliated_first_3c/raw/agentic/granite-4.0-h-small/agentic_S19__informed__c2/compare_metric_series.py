import os
from observability_client import ObservabilityClient


def compare_metric_series(
    metric_name,
    resource_a,
    resource_b,
    dimension_filter_a=None,
    dimension_filter_b=None,
    start_time=None,
    end_time=None,
):
    """Compare metric values for two resources or dimension filters over the same window.

    Args:
        metric_name (str): The name of the metric.
        resource_a (str): Identifier for the first resource.
        resource_b (str): Identifier for the second resource.
        dimension_filter_a (dict, optional): Filters to apply for resource A.
        dimension_filter_b (dict, optional): Filters to apply for resource B.
        start_time (int, optional): Unix timestamp for start of window (seconds).
        end_time (int, optional): Unix timestamp for end of window (seconds).

    Returns:
        dict: JSON response containing comparison results.
    """
    client = ObservabilityClient()
    payload = {
        "metric": metric_name,
        "resourceA": resource_a,
        "resourceB": resource_b,
        "filtersA": dimension_filter_a or {},
        "filtersB": dimension_filter_b or {},
    }
    if start_time:
        payload["start"] = start_time
    if end_time:
        payload["end"] = end_time
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/compare", json=payload
    )
    return response
