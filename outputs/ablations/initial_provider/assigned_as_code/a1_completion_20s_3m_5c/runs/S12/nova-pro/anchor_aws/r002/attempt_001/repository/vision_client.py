import boto3


def get_vision_client(config=None):
    config = config or {}
    return boto3.client("rekognition", region_name=config.get("region"))