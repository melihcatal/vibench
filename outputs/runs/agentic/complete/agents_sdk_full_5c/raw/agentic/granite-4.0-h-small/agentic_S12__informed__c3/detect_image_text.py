# detect_image_text.py
from typing import List
import os
from .vision_client import get_vision_client
from .vision_models import prepare_image_bytes, extract_text
from google.cloud.vision_v1.types import Feature, Feature_Type


def detect_image_text(image_bytes: bytes) -> List[str]:
    """Detect OCR text inside an image using Google Cloud Vision."""
    client = get_vision_client()
    feature = Feature(type_=Feature_Type.DOCUMENT_TEXT_DETECTION)
    request = prepare_image_bytes(image_bytes)
    request["features"].append(feature)

    response = client.annotate_image(request)
    return extract_text(response)
