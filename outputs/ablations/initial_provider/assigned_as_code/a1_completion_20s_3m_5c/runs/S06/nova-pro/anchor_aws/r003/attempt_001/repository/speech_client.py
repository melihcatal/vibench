import boto3


def get_speech_client(config=None):
    config = config or {}
    return boto3.client("polly", region_name=config.get("region"))