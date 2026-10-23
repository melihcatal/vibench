from datetime import datetime, timezone

import boto3

from observability_client import load_observability_config
from observability_models import cloudwatch_dimensions


def aggregate_metric_stats(payload, config=None):
    cfg = load_observability_config(config)
    client = boto3.client("cloudwatch", region_name=cfg.get("region"))
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=payload["metric"],
        Dimensions=cloudwatch_dimensions(payload.get("dimensions", cfg.get("dimensions", {}))),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cfg.get("period_seconds", payload.get("period_seconds", 60)),
        Statistics=payload.get("statistics", ["Average", "Sum", "Minimum", "Maximum"]),
    )
    datapoints = response.get("Datapoints", [])
    values = [float(point.get("Average", point.get("Sum", 0.0))) for point in datapoints if point.get("Average") is not None or point.get("Sum") is not None]
    return {
        "metric": payload["metric"],
        "count": len(values),
        "average": sum(values) / len(values) if values else 0.0,
        "minimum": min(values) if values else 0.0,
        "maximum": max(values) if values else 0.0,
        "datapoints": sorted(values),
    }
