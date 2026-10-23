from datetime import timedelta

from observability_client import cloudwatch_client, load_observability_config
from observability_models import normalize_dimensions, utcnow, isoformat


def compare_metric_series(metric_name: str, left_dimensions=None, right_dimensions=None, minutes: int = 60, namespace: str = None, statistic: str = "Average", period: int = 60):
    cfg = load_observability_config()
    namespace = namespace or cfg["metric_namespace"]
    end_time = utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    left = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
        Dimensions=normalize_dimensions(left_dimensions),
    )
    right = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[statistic],
        Dimensions=normalize_dimensions(right_dimensions),
    )
    return {
        "namespace": namespace,
        "metric_name": metric_name,
        "start_time": isoformat(start_time),
        "end_time": isoformat(end_time),
        "left": left.get("Datapoints", []),
        "right": right.get("Datapoints", []),
    }
