import os
from typing import List
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import LabelDetectionResponse


def detect_labels(image_path: str) -> LabelDetectionResponse:
    """Detect labels in a static image using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    return LabelDetectionResponse(
        labels=[label.description for label in labels],
        confidence=[label.score for label in labels]
    )