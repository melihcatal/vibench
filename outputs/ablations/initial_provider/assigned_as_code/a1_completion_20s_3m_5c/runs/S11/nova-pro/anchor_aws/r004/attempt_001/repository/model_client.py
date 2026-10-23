import boto3


def get_bedrock_client(region=None):
    return boto3.client("bedrock-runtime", region_name=region)


def configure_model_client(config):
    return get_bedrock_client(region=config.get("region", "us-east-1"))