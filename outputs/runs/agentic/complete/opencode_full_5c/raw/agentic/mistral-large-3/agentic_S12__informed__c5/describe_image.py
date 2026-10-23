import os
from typing import Optional

from google.cloud import vision_v1
from google.cloud.vision_v1 import types


def describe_image(
    image_bytes: bytes,
    language: str = "en",
    max_results: int = 1,
) -> str:
    """
    Generates a short visual description for an image using Google Cloud Vision.

    Args:
        image_bytes: Bytes of the image to describe.
        language: Language code for the description.
        max_results: Maximum number of descriptions to return.

    Returns:
        A short visual description of the image.
    """
    client = vision_v1.ImageAnnotatorClient()

    image = types.Image(content=image_bytes)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if not labels:
        return "No description available."

    # Use the first label as a simple description
    return f"An image of {labels[0].lower()}"
