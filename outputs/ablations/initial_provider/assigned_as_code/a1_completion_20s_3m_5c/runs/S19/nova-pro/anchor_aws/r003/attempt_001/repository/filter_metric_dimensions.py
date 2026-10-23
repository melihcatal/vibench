from datetime import datetime, timezone

import boto3

def filter_metric_dimensions(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(Namespace=config["namespace"], MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60), Statistics=["Average"])
    points = [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response["Datapoints"]]
    return {"points": sorted(points, key=lambda p: p["timestamp"])}