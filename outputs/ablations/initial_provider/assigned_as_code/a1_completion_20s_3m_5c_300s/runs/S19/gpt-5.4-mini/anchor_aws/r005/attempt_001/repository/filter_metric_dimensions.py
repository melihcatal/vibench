from observability_client import cloudwatch_client
from observability_models import build_dimensions, normalize_datapoints, to_utc_datetime


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = cloudwatch_client(config)
    dimensions = dict(config.get("dimensions", {}))
    dimensions.update(payload.get("dimensions", {}))
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=build_dimensions(dimensions),
        StartTime=to_utc_datetime(payload["start_time"]),
        EndTime=to_utc_datetime(payload["end_time"]),
        Period=config.get("period_seconds", 60),
        Statistics=["Average"],
    )
    return {"points": normalize_datapoints(response.get("Datapoints", []), "Average")}
