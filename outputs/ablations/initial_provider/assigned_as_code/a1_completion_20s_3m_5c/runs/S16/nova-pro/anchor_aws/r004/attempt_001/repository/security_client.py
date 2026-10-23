import boto3


def get_secrets_client(config=None):
    config = config or {}
    region = config.get("region", "us-west-2")
    return boto3.client("secretsmanager", region_name=region)