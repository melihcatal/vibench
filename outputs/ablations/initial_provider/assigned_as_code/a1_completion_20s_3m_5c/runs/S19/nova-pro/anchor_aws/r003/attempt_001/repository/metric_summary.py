from datetime import datetime, timezone

import boto3

def metric_summary(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(Namespace=config["namespace"], MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60), Statistics=["Average"])
    points = [{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response["Datapoints"]]
    sorted_points = sorted(points, key=lambda p: p["timestamp"])
    if len(sorted_points) > 0:
        first_point = sorted_points[0]
        last_point = sorted_points[-1]
        trend = (last_point["value"] - first_point["value"]) / (last_point["timestamp"] - first_point["timestamp"])
        return {"trend": trend, "first_point": first_point, "last_point": last_point}
    else:
        return {"trend": None, "first_point": None, "last_point": None}