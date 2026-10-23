import boto3


def get_client(config):
    return boto3.client("logs", region_name=config.get("region"))