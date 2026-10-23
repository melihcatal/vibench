from datetime import datetime, timezone

import boto3


def compare_metric_series(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response1 = client.get_metric_statistics(Namespace=config["namespace"], MetricName=payload["metric1"],
        Dimensions=[{"Name": k, "Value": v} for k, v in payload.get("dimensions1", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60), Statistics=["Average"])
    response2 = client.get_metric_statistics(Namespace=config["namespace"], MetricName=payload["metric2"],
        Dimensions=[{"Name": k, "Value": v} for k, v in payload.get("dimensions2", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60), Statistics=["Average"])
    points1 = [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response1["Datapoints"]]
    points2 = [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response2["Datapoints"]]
    return {"points1": sorted(points1, key=lambda p: p["timestamp"]), "points2": sorted(points2, key=lambda p: p["timestamp"])}