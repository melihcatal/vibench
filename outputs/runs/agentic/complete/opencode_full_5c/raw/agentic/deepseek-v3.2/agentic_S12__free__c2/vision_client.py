import os
from google.cloud import vision
import openai
from typing import Optional


def get_vision_client():
    """Initialize and return Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    client = vision.ImageAnnotatorClient()
    return client


def get_openai_client():
    """Initialize and return OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    client = openai.OpenAI(api_key=api_key)
    return client


def get_aws_client():
    """Initialize and return AWS client for Rekognition."""
    import boto3

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials environment variables not set")

    client = boto3.client(
        "rekognition",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )
    return client


def normalize_image_path(image_path: str) -> str:
    """Normalize image path and check if file exists."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not os.path.isfile(image_path):
        raise ValueError(f"Path is not a file: {image_path}")

    return os.path.abspath(image_path)
