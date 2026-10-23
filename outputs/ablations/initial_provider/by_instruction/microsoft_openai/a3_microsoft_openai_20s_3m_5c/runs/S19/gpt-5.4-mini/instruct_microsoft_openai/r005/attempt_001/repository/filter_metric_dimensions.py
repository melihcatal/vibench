from datetime import datetime

from observability_client import ObservabilityClient
from observability_models import MetricWindowRequest, normalize_dimensions


def filter_metric_dimensions(metric_name: str, start_time: datetime, end_time: datetime, dimensions: dict[str, str]):
    client = ObservabilityClient()
    request = MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=normalize_dimensions(dimensions))
    return client.post_json("/metrics/filter", request.to_dict())
