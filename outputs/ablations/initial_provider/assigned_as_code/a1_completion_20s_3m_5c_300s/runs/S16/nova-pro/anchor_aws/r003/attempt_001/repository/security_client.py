import boto3


def get_secretsmanager_client(config=None):
    config = config or {}
    region_name = config.get("region")
    return boto3.client("secretsmanager", region_name=region_name)