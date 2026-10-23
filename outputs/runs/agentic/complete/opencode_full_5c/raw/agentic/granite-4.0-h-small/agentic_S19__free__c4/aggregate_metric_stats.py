# [SAME-SCENARIO] aggregate_metric_stats.py
import observability_client as client


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str):
    """Retrieve aggregated statistics (sum, avg, min, max) for a metric over a time window.
    Uses the hypothetical Managed Metrics Monitoring service (e.g., Datadog).
    """
    payload = {
        "metric": metric_name,
        "start": start_time,
        "end": end_time,
    }
    response = client.aggregate(metric=metric_name, start=start_time, end=end_time)
    return response
