import statistics

from observability_client import cloudwatch_client
from observability_models import build_dimensions, normalize_datapoints, to_utc_datetime


def metric_summary(payload, config=None):
    config = config or {}
    client = cloudwatch_client(config)
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=build_dimensions(config.get("dimensions")),
        StartTime=to_utc_datetime(payload["start_time"]),
        EndTime=to_utc_datetime(payload["end_time"]),
        Period=config.get("period_seconds", 300),
        Statistics=["Average"],
    )
    points = normalize_datapoints(response.get("Datapoints", []), "Average")
    values = [point["value"] for point in points]
    return {"trend": values[-1] - values[0] if len(values) > 1 else 0.0, "median": statistics.median(values) if values else 0.0, "points": points}
