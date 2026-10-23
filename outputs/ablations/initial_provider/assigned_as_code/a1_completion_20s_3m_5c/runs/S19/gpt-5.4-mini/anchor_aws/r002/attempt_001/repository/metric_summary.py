from datetime import datetime, timezone

import boto3

from observability_models import datapoints_to_series, normalize_dimensions


def metric_summary(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=normalize_dimensions(config.get("dimensions")),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=["Average"],
    )
    series = datapoints_to_series(response.get("Datapoints", []))
    if not series:
        return {"trend": "flat", "anomalies": [], "points": []}
    values = [point["value"] for point in series]
    trend = "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "flat"
    anomalies = [point for point in series if point["value"] > (sum(values) / len(values)) * 1.5]
    return {"trend": trend, "anomalies": anomalies, "points": series}
