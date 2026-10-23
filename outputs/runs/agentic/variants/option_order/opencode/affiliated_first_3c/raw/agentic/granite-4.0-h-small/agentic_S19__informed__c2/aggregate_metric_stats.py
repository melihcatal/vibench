import os
from observability_client import ObservabilityClient


def aggregate_metric_stats(metric_name, start_time, end_time):
    """Retrieve aggregated statistics for a metric over a time window.

    Args:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp for start of window (seconds).
        end_time (int): Unix timestamp for end of window (seconds).

    Returns:
        dict: JSON response containing aggregated statistics.
    """
    client = ObservabilityClient()
    payload = {"metric": metric_name, "start": start_time, "end": end_time}
    response = client.rest_call(
        method="POST", endpoint="/api/v1/metrics/aggregate", json=payload
    )
    return response
