import boto3


def get_vision_client():
    return boto3.client("rekognition")
