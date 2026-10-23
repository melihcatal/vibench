import boto3


def key_usage_summary(config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    response = client.list_keys()
    return response['Keys']