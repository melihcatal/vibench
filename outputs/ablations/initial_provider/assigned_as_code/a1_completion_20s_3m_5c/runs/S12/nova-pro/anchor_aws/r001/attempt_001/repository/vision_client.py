import boto3


def get_vision_client(config=None):
    config = config or {}
    region = config.get("region", "us-west-2")
    return boto3.client("rekognition", region_name=region)