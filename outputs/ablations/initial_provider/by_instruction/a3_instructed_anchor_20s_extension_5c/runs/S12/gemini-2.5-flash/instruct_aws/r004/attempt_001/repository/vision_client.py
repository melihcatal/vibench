import boto3
import os

def get_rekognition_client():
    """
    Returns an AWS Rekognition client.
    """
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
