from datetime import datetime

from observability_client import ObservabilityClient
from observability_models import MetricWindowRequest


def query_metric_window(metric_name: str, start_time: datetime, end_time: datetime, resource: str | None = None, dimensions: dict[str, str] | None = None):
    client = ObservabilityClient()
    request = MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource=resource, dimensions=dimensions or {})
    return client.query_metric_series(request)
