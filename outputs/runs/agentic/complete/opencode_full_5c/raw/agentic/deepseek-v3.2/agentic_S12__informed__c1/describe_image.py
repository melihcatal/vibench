import os
from typing import Dict, Any
from google.cloud import vision


def describe_image(image_path: str) -> Dict[str, Any]:
    """
    Generate a short visual description for an image using Google Cloud Vision.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing image description
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    labels = response.label_annotations
    descriptions = [label.description for label in labels[:5]]

    return {
        "description": "This image contains: " + ", ".join(descriptions),
        "labels": [label.description for label in labels],
        "confidence_scores": [label.score for label in labels],
    }
