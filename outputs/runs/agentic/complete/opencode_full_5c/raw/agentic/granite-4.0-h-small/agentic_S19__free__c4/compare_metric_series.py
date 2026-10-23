# [SAME-SCENARIO] compare_metric_series.py
import observability_client as client


def compare_metric_series(
    metric_name: str, resource_a: str, resource_b: str, start_time: str, end_time: str
):
    """Compare metric values for two resources or dimension filters over the same window.
    Uses the hypothetical Managed Metrics Monitoring service (e.g., Datadog).
    """
    payload = {
        "metric": metric_name,
        "resource_a": resource_a,
        "resource_b": resource_b,
        "start": start_time,
        "end": end_time,
    }
    response = client.compare(
        metric=metric_name,
        resource_a=resource_a,
        resource_b=resource_b,
        start=start_time,
        end=end_time,
    )
    return response
