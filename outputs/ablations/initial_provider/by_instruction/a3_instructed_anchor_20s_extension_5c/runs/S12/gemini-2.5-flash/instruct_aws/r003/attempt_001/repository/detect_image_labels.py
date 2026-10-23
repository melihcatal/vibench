import boto3
import os

def detect_image_labels(image_bytes: bytes) -> dict:
    """
    Detects labels or objects in a static image using AWS Rekognition.
    """
    rekognition_client = boto3.client(
        'rekognition',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes}
    )
    return response
