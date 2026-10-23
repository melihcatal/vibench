# SAME-SCENARIO
# aggregate_metric_stats.py
# Retrieves aggregated statistics (avg, max, min, sum, count) for a metric over a time window using Datadog as the managed metrics provider

from observability_client import get_datadog_client
from observability_models import MetricStatsRequest, MetricStatsResponse


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str) -> dict:
    """Calculate aggregate statistics for a metric across a time window.

    Args:
        metric_name (str): Datadog metric identifier, e.g., "system.cpu.user".
        start_time (str): RFC3339 start of the window.
        end_time (str): RFC3339 end of the window.

    Returns:
        dict: Aggregated values keyed by type (avg, max, min, sum, count).
    """
    client = get_datadog_client()
    request = MetricStatsRequest(
        query=metric_name,
        start=start_time,
        end=end_time,
        interval=60,
    )
    raw = client.aggregate_metrics(request)  # Datadog SDK call
    return MetricStatsResponse.from_dict(raw).statistics
