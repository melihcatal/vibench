import boto3

from observability_client import load_observability_config


def metric_summary(payload, config=None):
    config = load_observability_config(config)
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=payload["start_time"],
        EndTime=payload["end_time"],
        Period=config.get("period_seconds", 60),
        Statistics=["Average", "Maximum"],
    )
    points = response["Datapoints"]
    return {"metric": payload["metric"], "count": len(points), "latest": points[-1]["Average"] if points else None}
