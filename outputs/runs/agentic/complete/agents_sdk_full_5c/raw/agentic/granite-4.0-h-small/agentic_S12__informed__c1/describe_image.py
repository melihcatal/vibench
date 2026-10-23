import os
from vision_client import VisionClient

def describe_image(image_path: str) -> str:
    """Generate a short visual description for an image using Alibaba Cloud Vision API.
    Returns a concise description string.
    """
    with open(image_path, "rb") as img_file:
        result = VisionClient().vision_client.describe_image(image=img_file.read())
    # Assume the API returns a top-level 'description' field
    return result.get('description', 'No description available.')
