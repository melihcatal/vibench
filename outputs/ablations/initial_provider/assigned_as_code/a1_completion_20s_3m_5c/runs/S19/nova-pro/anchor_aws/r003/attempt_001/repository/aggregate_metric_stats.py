from datetime import datetime, timezone

import boto3

def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(Namespace=config["namespace"], MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60), Statistics=["Sum", "Minimum", "Maximum", "SampleCount"])
    stats = {"sum": response["Datapoints"][0].get("Sum", None),
              "min": response["Datapoints"][0].get("Minimum", None),
              "max": response["Datapoints"][0].get("Maximum", None),
              "count": response["Datapoints"][0].get("SampleCount", None)}
    return stats