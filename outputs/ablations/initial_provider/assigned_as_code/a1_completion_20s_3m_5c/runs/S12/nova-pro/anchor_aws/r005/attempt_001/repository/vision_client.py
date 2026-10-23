import boto3


def get_vision_client(region):
    return boto3.client("rekognition", region_name=region)


def get_translate_client(region):
    return boto3.client("translate", region_name=region)