import os
from vision_client import GoogleVisionClient


def describe_image(image_path: str) -> str:
    """
    Generates a short visual description for an image using Google Cloud Vision.
    """
    client = GoogleVisionClient()
    return client.describe_image(image_path)
