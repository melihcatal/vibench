from datetime import datetime

from observability_client import cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, MetricWindowResponse, parse_cloudwatch_datapoints


def filter_metric_dimensions(metric_name: str, start_time: datetime, end_time: datetime, dimensions: dict | None = None, namespace: str | None = None, period: int = 60, statistic: str = "Average") -> MetricWindowResponse:
    cfg = load_observability_config()
    request = MetricWindowRequest(namespace=namespace or cfg["cloudwatch_namespace"], metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, statistics=[statistic], dimensions=dimensions)
    client = cloudwatch_client()
    response = client.get_metric_statistics(**request.to_cloudwatch_kwargs())
    return MetricWindowResponse(namespace=request.namespace, metric_name=metric_name, points=parse_cloudwatch_datapoints(response.get("Datapoints", []), statistic), unit=response.get("Label"), dimensions=request.dimensions)
