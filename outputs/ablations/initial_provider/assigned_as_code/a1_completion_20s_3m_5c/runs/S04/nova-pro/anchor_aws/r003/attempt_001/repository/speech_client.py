import boto3


def get_transcribe_client(config=None):
    config = config or {}
    region = config.get("region", "us-west-2")
    return boto3.client("transcribe", region_name=region)
