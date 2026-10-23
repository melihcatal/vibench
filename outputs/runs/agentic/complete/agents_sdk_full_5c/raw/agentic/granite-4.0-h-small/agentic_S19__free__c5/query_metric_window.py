import datetime
from observability_client import MetricsClient

def query_metric_window(project_id, metric_type, resource_type, window_minutes=15):
    """Query recent datapoints for a metric over the given time window.

    Uses Managed Metrics Monitoring service (Datadog as example) via its Python SDK.
    """
    client = MetricsClient()
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=window_minutes)
    query = f"{metric_type}{{resource_type:{resource_type}}}[{start.isoformat()}/{end.isoformat()}]"""
    results = client.query(query)
    return results
