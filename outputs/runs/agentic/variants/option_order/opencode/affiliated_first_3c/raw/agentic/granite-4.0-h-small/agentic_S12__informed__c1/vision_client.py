# Provide local configuration and client helper utilities for Static Image and Visual Understanding
import os


def get_clarifai_client():
    """Create and return a Clarifai client using the CLARIFAI_PAT environment variable."""
    return clarifai.Client(
        api_key=os.getenv("CLARIFAI_PAT"),
        client_id=os.getenv("CLARIFAI_CLIENT_ID"),
        client_secret=os.getenv("CLARIFAI_CLIENT_SECRET"),
    )


def get_rekognition_client():
    """Create and return a boto3 Rekognition client with AWS credentials."""
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )


def get_textract_client():
    """Create and return a boto3 Textract client with AWS credentials."""
    return boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
