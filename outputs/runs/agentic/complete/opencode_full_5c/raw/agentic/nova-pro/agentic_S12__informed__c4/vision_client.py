import boto3


def get_rekognition_client():
    return boto3.client("rekognition")
