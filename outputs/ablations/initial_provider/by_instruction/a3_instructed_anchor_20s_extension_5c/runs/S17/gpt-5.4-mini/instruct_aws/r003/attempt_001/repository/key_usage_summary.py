import boto3


def key_usage_summary(key_id, region_name=None):
    cloudwatch = boto3.client("cloudwatch", region_name=region_name)
    return {"provider": "aws-cloudwatch", "key_id": key_id, "metric_namespace": "AWS/KMS", "metrics": ["Decrypt", "Encrypt", "GenerateDataKey"]}
