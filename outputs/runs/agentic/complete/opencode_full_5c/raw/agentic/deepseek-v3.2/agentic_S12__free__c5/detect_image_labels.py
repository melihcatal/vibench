import os
from google.cloud import vision
from google.cloud.vision_v1 import types


def detect_image_labels(image_path: str) -> list:
    """Detect labels or objects in a static image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    return [
        {"description": label.description, "score": label.score} for label in labels
    ]
