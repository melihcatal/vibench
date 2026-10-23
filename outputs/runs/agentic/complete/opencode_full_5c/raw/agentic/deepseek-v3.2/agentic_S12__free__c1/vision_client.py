import os
from google.cloud import vision
from typing import Tuple, Optional


def get_vision_client():
    """Initialize and return Google Cloud Vision client."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return vision.ImageAnnotatorClient()


def get_azure_vision_key() -> str:
    """Get Azure Computer Vision subscription key."""
    key = os.getenv("AZURE_VISION_KEY")
    if not key:
        raise ValueError("AZURE_VISION_KEY environment variable not set")
    return key


def get_azure_vision_endpoint() -> str:
    """Get Azure Computer Vision endpoint."""
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    if not endpoint:
        raise ValueError("AZURE_VISION_ENDPOINT environment variable not set")
    return endpoint.rstrip("/")


def get_aws_credentials() -> Tuple[str, str, str]:
    """Get AWS credentials for Rekognition."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables not set"
        )

    return access_key, secret_key, region


def get_openai_api_key() -> str:
    """Get OpenAI API key."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key


def get_google_translate_key() -> str:
    """Get Google Cloud Translation API key."""
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY environment variable not set")
    return api_key


def get_aws_s3_credentials() -> Tuple[str, str, str]:
    """Get AWS credentials for S3."""
    access_key = os.getenv("AWS_S3_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_S3_REGION", "us-east-1")

    if not access_key or not secret_key:
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError("AWS credentials for S3 not found in environment variables")

    return access_key, secret_key, region
