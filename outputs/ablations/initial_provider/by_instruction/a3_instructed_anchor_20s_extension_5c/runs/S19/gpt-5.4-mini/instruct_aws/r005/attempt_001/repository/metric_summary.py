from datetime import timedelta

from observability_client import cloudwatch_client, load_observability_config
from observability_models import normalize_dimensions, utcnow


def metric_summary(metric_name: str, minutes: int = 120, namespace: str = None, dimensions=None):
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
        Period=60,
        Statistics=["Average", "Maximum"],
        Dimensions=normalize_dimensions(dimensions),
    )
    datapoints = response.get("Datapoints", [])
    return {"provider": "aws_cloudwatch", "metric_name": metric_name, "datapoint_count": len(datapoints), "datapoints": datapoints}
