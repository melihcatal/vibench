import boto3


def get_client(config):
    region = config.get("region", "us-east-1")
    return boto3.client("comprehend", region_name=region)