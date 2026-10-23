from datetime import datetime, timezone

import boto3

from observability_models import datapoints_to_series, normalize_dimensions


def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    dimensions = dict(config.get("dimensions", {}))
    dimensions.update(payload.get("dimensions", {}))
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=normalize_dimensions(dimensions),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=["Average"],
    )
    return {"points": datapoints_to_series(response.get("Datapoints", []))}
