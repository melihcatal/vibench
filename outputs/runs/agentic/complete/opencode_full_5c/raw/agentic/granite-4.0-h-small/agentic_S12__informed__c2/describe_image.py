# [SAME-SCENARIO] describe_image.py

import os
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Azure AI Vision SDK.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Generated description of the image content.
    """
    client = VisionClient()
    return client.describe_image(image_path)
