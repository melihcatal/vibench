from datetime import datetime, timezone

import boto3

from observability_client import load_observability_config
from observability_models import cloudwatch_dimensions, datapoints_to_series


def _series(client, cfg, metric, start_time, end_time, dimensions):
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric,
        Dimensions=cloudwatch_dimensions(dimensions),
        StartTime=start_time,
        EndTime=end_time,
        Period=cfg.get("period_seconds", 60),
        Statistics=[cfg.get("statistic", "Average")],
    )
    return datapoints_to_series(response.get("Datapoints", []))


def compare_metric_series(payload, config=None):
    cfg = load_observability_config(config)
    client = boto3.client("cloudwatch", region_name=cfg.get("region"))
    start_time = datetime.fromtimestamp(payload["start_time"], timezone.utc)
    end_time = datetime.fromtimestamp(payload["end_time"], timezone.utc)
    left = _series(client, cfg, payload["metric"], start_time, end_time, payload.get("left_dimensions", {}))
    right = _series(client, cfg, payload["metric"], start_time, end_time, payload.get("right_dimensions", {}))
    return {"metric": payload["metric"], "left": left, "right": right}
