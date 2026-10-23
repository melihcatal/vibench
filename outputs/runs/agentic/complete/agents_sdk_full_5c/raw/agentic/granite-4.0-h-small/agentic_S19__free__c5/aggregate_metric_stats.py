import datetime
from observability_client import MetricsClient

def aggregate_metric_stats(project_id, metric_type, resource_type, window_minutes=60):
    """Retrieve aggregated statistics (sum, avg, min, max) for a metric over a time window.

    Uses Managed Metrics Monitoring service (Datadog as example) via its Python SDK.
    """
    client = MetricsClient()
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=window_minutes)
    query = f"{metric_type}{{resource_type:{resource_type}}}.as_count()"
    stats = client.query(query, start=start, end=end, aggregation='sum')
    return stats
