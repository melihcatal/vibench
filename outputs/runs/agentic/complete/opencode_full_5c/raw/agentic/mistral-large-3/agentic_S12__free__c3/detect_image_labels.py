import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import LabelDetectionResponse


def detect_image_labels(image_path: str) -> LabelDetectionResponse:
    """Detects labels in a static image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return LabelDetectionResponse(
        provider="google_cloud_vision",
        model="label_detection",
        labels=[label.description for label in labels],
        confidence_scores=[label.score for label in labels],
    )
