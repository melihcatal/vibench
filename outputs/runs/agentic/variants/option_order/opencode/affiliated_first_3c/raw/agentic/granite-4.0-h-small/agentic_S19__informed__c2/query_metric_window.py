import os
from observability_client import ObservabilityClient


def query_metric_window(metric_name, start_time, end_time, window_seconds):
    """Query recent datapoints for a named metric over a time window.

    Args:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp for start of window (seconds).
        end_time (int): Unix timestamp for end of window (seconds).
        window_seconds (int): Duration of the window in seconds.

    Returns:
        dict: JSON response containing datapoints.
    """
    client = ObservabilityClient()
    payload = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
        "window": window_seconds,
    }
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/query", json=payload
    )
    return response
