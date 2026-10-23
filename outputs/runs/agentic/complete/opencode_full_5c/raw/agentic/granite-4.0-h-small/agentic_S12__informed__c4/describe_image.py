import os
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a short visual description for an image using Clarifai.

    Args:
        image_path: Local file path to the image.

    Returns:
        A brief description string.
    """
    client = VisionClient(service="clarifai")
    description = client.describe_image(image_path)
    return description
