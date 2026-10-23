# [SAME-SCENARIO] filter_metric_dimensions.py
import observability_client as client


def filter_metric_dimensions(metric_name: str, filter_expr: str):
    """Query metric data filtered by resource labels or dimensions.
    Uses the hypothetical Managed Metrics Monitoring service (e.g., Datadog).
    """
    payload = {
        "metric": metric_name,
        "filter": filter_expr,
    }
    response = client.filter(metric=metric_name, filter=filter_expr)
    return response
