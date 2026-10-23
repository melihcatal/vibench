# [SAME-SCENARIO] query_metric_window.py
import observability_client as client


def query_metric_window(metric_name: str, start_time: str, end_time: str):
    """Query recent datapoints for a metric within a time window.
    Uses the hypothetical Managed Metrics Monitoring service (e.g., Datadog).
    """
    payload = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
    }
    response = client.query(metric=metric_name, start=start_time, end=end_time)
    return response
