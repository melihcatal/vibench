from datetime import datetime, timedelta, timezone

from observability_client import cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, MetricWindowResponse, parse_cloudwatch_datapoints


def query_metric_window(metric_name: str, start_time: datetime, end_time: datetime, namespace: str | None = None, period: int = 60, dimensions=None, statistic: str = "Average") -> MetricWindowResponse:
    cfg = load_observability_config()
    request = MetricWindowRequest(
        namespace=namespace or cfg["cloudwatch_namespace"],
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=[statistic],
        dimensions=dimensions,
    )
    client = cloudwatch_client()
    response = client.get_metric_statistics(**request.to_cloudwatch_kwargs())
    points = parse_cloudwatch_datapoints(response.get("Datapoints", []), statistic)
    return MetricWindowResponse(
        namespace=request.namespace,
        metric_name=metric_name,
        points=points,
        unit=response.get("Label"),
        dimensions=request.dimensions,
    )


def recent_metric_window(metric_name: str, minutes: int = 15, namespace: str | None = None, period: int = 60, dimensions=None) -> MetricWindowResponse:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return query_metric_window(metric_name, start_time, end_time, namespace=namespace, period=period, dimensions=dimensions)
