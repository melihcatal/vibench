import os
from google.cloud import vision


def detect_image_labels(image_path):
    """Detects labels or objects in a static image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision error: {response.error.message}")

    return [
        {"description": label.description, "score": label.score, "mid": label.mid}
        for label in labels
    ]
