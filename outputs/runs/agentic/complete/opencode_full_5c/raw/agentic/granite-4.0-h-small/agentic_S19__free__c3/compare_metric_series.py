# SAME-SCENARIO
# compare_metric_series.py
# Compares metric values for two resources or dimension filters over the same window using Datadog as the managed metrics provider

from observability_client import get_datadog_client
from observability_models import MetricComparisonRequest, MetricComparisonResponse


def compare_metric_series(
    metric: str, resource_a: str, resource_b: str, window: str
) -> dict:
    """
    Compare two series of a metric over the same time window.

    Args:
        metric (str): Datadog metric, e.g., "system.cpu.user".
        resource_a (str): First resource identifier (host, container, etc.).
        resource_b (str): Second resource identifier.
        window (str): ISO8601 duration string or RFC3339 range, e.g., "10m" or "2024-03-01T00:00:00Z/2024-03-01T00:10:00Z".

    Returns:
        dict: Difference, ratio, and basic stats for the two series.
    """
    client = get_datadog_client()
    request = MetricComparisonRequest(
        query=f"{metric}{{*}} by {{host}}",
        resource_a=resource_a,
        resource_b=resource_b,
        window=window,
    )
    raw = client.compare_series(request)  # Datadog SDK call
    return MetricComparisonResponse.from_dict(raw).comparison
