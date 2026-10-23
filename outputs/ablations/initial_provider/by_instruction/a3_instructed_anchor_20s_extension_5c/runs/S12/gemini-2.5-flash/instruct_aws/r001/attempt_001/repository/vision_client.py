import os
import boto3
from google.cloud import vision

def get_aws_rekognition_client():
    """
    Provides an AWS Rekognition client.
    """
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

def get_google_vision_client():
    """
    Provides a Google Cloud Vision API client.
    """
    # Google Cloud client automatically picks up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    return vision.ImageAnnotatorClient()
