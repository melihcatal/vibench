import boto3


def get_bedrock_client(config=None):
    config = config or {}
    return boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))