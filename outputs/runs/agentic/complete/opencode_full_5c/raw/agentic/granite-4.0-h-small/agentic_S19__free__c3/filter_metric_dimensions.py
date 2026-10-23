# SAME-SCENARIO
# filter_metric_dimensions.py
# Queries metric data filtered by resource labels/dimensions using Datadog as the managed metrics provider

from observability_client import get_datadog_client
from observability_models import MetricFilterRequest, MetricFilterResponse


def filter_metric_dimensions(metric_name: str, dimension_filters: dict) -> list:
    """
    Retrieve datapoints for a metric limited to specific dimension values.

    Args:
        metric_name (str): Datadog metric identifier, e.g., "system.net.bytes_rcvd".
        dimension_filters (dict): Mapping of dimension keys to lists of allowed values.
            Example: {"host": ["web-01", "web-02"], "region": ["us-east-1"]}

    Returns:
        list: Datapoints matching the dimension constraints.
    """
    client = get_datadog_client()
    request = MetricFilterRequest(
        query=metric_name,
        filters=dimension_filters,
        start="-10m",
        end="now",
    )
    raw = client.filter_metrics(request)  # Datadog SDK call
    return MetricFilterResponse.from_dict(raw).datapoints
