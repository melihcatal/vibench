from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import TextDetectionResponse, normalize_text_annotation


def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Detects text appearing inside an image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return normalize_text_annotation(texts)
