import boto3


def key_usage_summary(key_id: str):
    cloudwatch = boto3.client("cloudwatch")
    return cloudwatch.list_metrics(
        Namespace="AWS/KMS", Dimensions=[{"Name": "KeyId", "Value": key_id}]
    )
