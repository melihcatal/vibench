# detect_image_labels.py
import os
from google.cloud import vision


def detect_image_labels(image_path):
    """Detect labels/objects in a static image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]
