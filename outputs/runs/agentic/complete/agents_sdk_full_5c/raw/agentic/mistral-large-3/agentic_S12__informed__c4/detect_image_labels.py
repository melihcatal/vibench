import os
from typing import List, Dict
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from vision_client import get_vision_client
from vision_models import LabelDetectionResponse


def detect_image_labels(image_path: str) -> LabelDetectionResponse:
    """Detects labels in a static image using Google Cloud Vision."""
    client = get_vision_client(vision_v1.ImageAnnotatorClient)

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return LabelDetectionResponse(
        labels=[label.description for label in labels],
        confidence=[label.score for label in labels]
    )