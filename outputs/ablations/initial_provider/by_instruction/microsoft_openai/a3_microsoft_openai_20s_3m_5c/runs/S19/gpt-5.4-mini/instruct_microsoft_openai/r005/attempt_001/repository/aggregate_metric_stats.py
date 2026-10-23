from datetime import datetime

from observability_client import ObservabilityClient
from observability_models import MetricWindowRequest


def aggregate_metric_stats(metric_name: str, start_time: datetime, end_time: datetime, aggregation: str = "avg", resource: str | None = None, dimensions: dict[str, str] | None = None):
    client = ObservabilityClient()
    request = MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource=resource, dimensions=dimensions or {}, aggregation=aggregation)
    return client.post_json("/metrics/aggregate", request.to_dict())
