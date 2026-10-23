# describe_image.py
from typing import List
import os
from .vision_client import get_vision_client
from .vision_models import prepare_image_bytes, extract_text
from google.cloud.vision_v1.types import Feature, Feature_Type


def describe_image(image_bytes: bytes) -> str:
    """Generate a short visual description of an image using Google Cloud Vision OCR."""
    client = get_vision_client()
    # Use both LABEL_DETECTION and DOCUMENT_TEXT_DETECTION for richer output
    features = [
        Feature(type_=Feature_Type.LABEL_DETECTION),
        Feature(type_=Feature_Type.DOCUMENT_TEXT_DETECTION)
    ]
    request = prepare_image_bytes(image_bytes)
    request["features"].extend(features)

    response = client.annotate_image(request)
    # Prefer OCR text as a concise description, fallback to top label
    text = extract_text(response)
    description = " \n".join(text) if text else None
    if description:
        desc = description[:256]  # keep it short
    else:
        labels = extract_labels(response)
        desc = labels[0] if labels else "No description available"
    return desc
