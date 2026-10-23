import os
from typing import Tuple
from google.cloud import vision


def get_vision_client():
    """
    Get a Google Cloud Vision client.

    Returns:
        Initialized Google Cloud Vision client
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

    return vision.ImageAnnotatorClient()


def get_openai_api_key() -> str:
    """
    Get OpenAI API key from environment.

    Returns:
        OpenAI API key
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key


def get_aws_credentials() -> Tuple[str, str, str]:
    """
    Get AWS credentials from environment.

    Returns:
        Tuple of (access_key, secret_key, region)
    """
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    return access_key, secret_key, region


def get_azure_vision_key() -> Tuple[str, str]:
    """
    Get Azure Computer Vision credentials from environment.

    Returns:
        Tuple of (subscription_key, endpoint)
    """
    subscription_key = os.getenv("AZURE_VISION_KEY")
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError(
            "AZURE_VISION_KEY and AZURE_VISION_ENDPOINT environment variables must be set"
        )

    return subscription_key, endpoint


def normalize_image_path(image_path: str) -> str:
    """
    Normalize image path and check if file exists.

    Args:
        image_path: Path to image file

    Returns:
        Normalized absolute path
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    return os.path.abspath(image_path)
