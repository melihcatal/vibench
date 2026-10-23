from datetime import datetime, timezone

import boto3

from observability_client import load_observability_config
from observability_models import cloudwatch_dimensions, datapoints_to_series


def filter_metric_dimensions(payload, config=None):
    cfg = load_observability_config(config)
    client = boto3.client("cloudwatch", region_name=cfg.get("region"))
    dimensions = payload.get("dimensions", payload.get("filters", cfg.get("dimensions", {})))
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=payload["metric"],
        Dimensions=cloudwatch_dimensions(dimensions),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cfg.get("period_seconds", payload.get("period_seconds", 60)),
        Statistics=[payload.get("statistic", "Average")],
    )
    return {"metric": payload["metric"], "dimensions": dimensions, "points": datapoints_to_series(response.get("Datapoints", []))}
