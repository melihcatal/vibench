import os
from observability_client import ObservabilityClient


def filter_metric_dimensions(metric_name, dimensions, start_time=None, end_time=None):
    """Query metric data filtered by resource labels or dimensions.

    Args:
        metric_name (str): The name of the metric.
        dimensions (dict): Key-value pairs for resource labels or dimensions.
        start_time (int, optional): Unix timestamp for start of window (seconds).
        end_time (int, optional): Unix timestamp for end of window (seconds).

    Returns:
        dict: JSON response containing filtered datapoints.
    """
    client = ObservabilityClient()
    payload = {"metric": metric_name, "filters": dimensions}
    if start_time:
        payload["start"] = start_time
    if end_time:
        payload["end"] = end_time
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/filter", json=payload
    )
    return response
