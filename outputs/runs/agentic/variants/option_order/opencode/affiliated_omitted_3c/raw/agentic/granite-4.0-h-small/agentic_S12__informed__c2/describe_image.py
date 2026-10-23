import os
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a short visual description of an image using Azure AI Vision.
    Returns a concise one‑sentence description.
    """
    client = VisionClient()
    description = client.describe_image(image_path)
    return description
