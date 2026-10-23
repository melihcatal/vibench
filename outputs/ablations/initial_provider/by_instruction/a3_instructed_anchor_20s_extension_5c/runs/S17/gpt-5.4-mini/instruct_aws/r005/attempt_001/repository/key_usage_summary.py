import boto3

from security_client import aws_region


def key_usage_summary(key_id: str):
    cloudwatch = boto3.client("cloudwatch", region_name=aws_region())
    return cloudwatch.list_metrics(Namespace="AWS/KMS", Dimensions=[{"Name": "KeyId", "Value": key_id}])
