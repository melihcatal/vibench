from datetime import datetime

from observability_client import cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, parse_cloudwatch_datapoints


def compare_metric_series(metric_name: str, start_time: datetime, end_time: datetime, left_dimensions: dict | None = None, right_dimensions: dict | None = None, namespace: str | None = None, period: int = 60, statistic: str = "Average"):
    cfg = load_observability_config()
    client = cloudwatch_client()
    left_request = MetricWindowRequest(namespace=namespace or cfg["cloudwatch_namespace"], metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, statistics=[statistic], dimensions=left_dimensions)
    right_request = MetricWindowRequest(namespace=namespace or cfg["cloudwatch_namespace"], metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, statistics=[statistic], dimensions=right_dimensions)
    left = client.get_metric_statistics(**left_request.to_cloudwatch_kwargs())
    right = client.get_metric_statistics(**right_request.to_cloudwatch_kwargs())
    return {"left": parse_cloudwatch_datapoints(left.get("Datapoints", []), statistic), "right": parse_cloudwatch_datapoints(right.get("Datapoints", []), statistic)}
