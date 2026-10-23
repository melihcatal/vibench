import boto3


def get_observability_client(config=None):
    config = config or {}
    return boto3.client("logs", region_name=config.get("region"))
