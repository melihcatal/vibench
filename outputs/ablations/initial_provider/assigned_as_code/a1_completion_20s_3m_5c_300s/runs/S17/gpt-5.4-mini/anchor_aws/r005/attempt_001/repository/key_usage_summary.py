import boto3

from security_models import response_dict


def key_usage_summary(payload, config=None):
    config = config or {}
    cloudwatch = boto3.client("cloudwatch", region_name=config.get("region"))
    key_id = payload["key_id"]
    metrics = cloudwatch.list_metrics(Namespace="AWS/KMS", MetricName="Encrypt")
    return response_dict(key_id=key_id, metrics=metrics.get("Metrics", []))
