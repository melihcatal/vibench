from datetime import datetime

from observability_client import cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, MetricWindowResponse, parse_cloudwatch_datapoints


def aggregate_metric_stats(metric_name: str, start_time: datetime, end_time: datetime, namespace: str | None = None, period: int = 300, dimensions=None, statistics=None) -> MetricWindowResponse:
    cfg = load_observability_config()
    stats = statistics or ["Average", "Sum", "Minimum", "Maximum", "SampleCount"]
    request = MetricWindowRequest(
        namespace=namespace or cfg["cloudwatch_namespace"],
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=stats,
        dimensions=dimensions,
    )
    client = cloudwatch_client()
    response = client.get_metric_statistics(**request.to_cloudwatch_kwargs())
    points = []
    for stat in stats:
        points.extend(parse_cloudwatch_datapoints(response.get("Datapoints", []), stat))
    return MetricWindowResponse(namespace=request.namespace, metric_name=metric_name, points=points, unit=response.get("Label"), dimensions=request.dimensions)
