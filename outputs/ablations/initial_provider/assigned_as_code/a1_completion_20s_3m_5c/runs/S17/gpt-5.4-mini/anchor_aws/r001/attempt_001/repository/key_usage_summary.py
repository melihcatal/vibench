import boto3


def key_usage_summary(payload, config=None):
    config = config or {}
    cloudwatch = boto3.client("cloudwatch", region_name=config.get("region"))
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/KMS",
        MetricName="KeyUsage",
        Dimensions=[{"Name": "KeyId", "Value": config.get("key_id", "") }],
        StartTime=payload.get("start_time"),
        EndTime=payload.get("end_time"),
        Period=config.get("period", 3600),
        Statistics=["Sum"],
    )
    return {"datapoints": response.get("Datapoints", [])}
