from datetime import timedelta

from observability_client import cloudwatch_client, load_observability_config
from observability_models import normalize_dimensions, utcnow, isoformat


def aggregate_metric_stats(metric_name: str, minutes: int = 60, namespace: str = None, dimensions=None, period: int = 60):
    cfg = load_observability_config()
    namespace = namespace or cfg["metric_namespace"]
    end_time = utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        Dimensions=normalize_dimensions(dimensions),
    )
    return {
        "namespace": namespace,
        "metric_name": metric_name,
        "start_time": isoformat(start_time),
        "end_time": isoformat(end_time),
        "period": period,
        "datapoints": response.get("Datapoints", []),
    }
