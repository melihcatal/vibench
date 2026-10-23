from typing import List
import os
from google.cloud import vision
from vision_models import LabelDetectionResponse


def detect_image_labels(image_path: str) -> LabelDetectionResponse:
    """Detect labels in a static image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return LabelDetectionResponse(
        labels=[label.description for label in labels],
        confidence=[label.score for label in labels]
    )