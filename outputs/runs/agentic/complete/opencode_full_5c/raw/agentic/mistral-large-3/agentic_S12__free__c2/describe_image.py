import os
from vision_client import AWSVisionClient


def describe_image(image_path: str) -> str:
    """Generate a short visual description for an image using AWS Rekognition."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    client = AWSVisionClient()
    description = client.generate_image_description(image_bytes)

    if not description:
        return "No description available for this image."
    return description
