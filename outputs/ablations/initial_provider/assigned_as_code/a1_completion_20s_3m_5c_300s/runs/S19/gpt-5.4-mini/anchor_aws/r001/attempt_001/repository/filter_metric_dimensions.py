from datetime import datetime, timezone

from observability_client import load_config, cloudwatch_client
from observability_models import build_dimensions


def filter_metric_dimensions(payload, config=None):
    cfg = load_config(config)
    client = cloudwatch_client(config)
    dimensions = dict(cfg.dimensions)
    dimensions.update(payload.get("dimensions", {}))
    response = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=payload["metric"],
        Dimensions=build_dimensions(dimensions),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cfg.period_seconds,
        Statistics=["Average"],
    )
    return {"points": [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response.get("Datapoints", [])]}
