from datetime import datetime, timezone

import boto3

from observability_client import load_observability_config
from observability_models import cloudwatch_dimensions, datapoints_to_series


def metric_summary(payload, config=None):
    cfg = load_observability_config(config)
    client = boto3.client("cloudwatch", region_name=cfg.get("region"))
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=payload["metric"],
        Dimensions=cloudwatch_dimensions(payload.get("dimensions", cfg.get("dimensions", {}))),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cfg.get("period_seconds", 60),
        Statistics=["Average", "Minimum", "Maximum"],
    )
    points = datapoints_to_series(response.get("Datapoints", []))
    values = [point["value"] for point in points]
    return {"metric": payload["metric"], "trend": values[-1] - values[0] if len(values) > 1 else 0.0, "points": points}
