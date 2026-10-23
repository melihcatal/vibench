from datetime import datetime, timezone

import boto3

from observability_models import datapoints_to_series, normalize_dimensions


def _series(client, namespace, metric, dimensions, start_time, end_time, period_seconds):
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        Dimensions=normalize_dimensions(dimensions),
        StartTime=datetime.fromtimestamp(start_time, timezone.utc),
        EndTime=datetime.fromtimestamp(end_time, timezone.utc),
        Period=period_seconds,
        Statistics=["Average"],
    )
    return datapoints_to_series(response.get("Datapoints", []))


def compare_metric_series(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    left = _series(
        client,
        config["namespace"],
        payload["metric"],
        payload["left_dimensions"],
        payload["start_time"],
        payload["end_time"],
        config.get("period_seconds", 60),
    )
    right = _series(
        client,
        config["namespace"],
        payload["metric"],
        payload["right_dimensions"],
        payload["start_time"],
        payload["end_time"],
        config.get("period_seconds", 60),
    )
    return {"left": left, "right": right}
