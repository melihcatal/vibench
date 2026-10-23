import boto3


def get_translate_client(config=None):
    config = config or {}
    return boto3.client("translate", region_name=config.get("region"))