# score_image_safety.py
from typing import Dict
import os
from .vision_client import get_vision_client
from .vision_models import prepare_image_bytes, extract_safe_search
from google.cloud.vision_v1.types import Feature, Feature_Type


def score_image_safety(image_bytes: bytes) -> Dict:
    """Check an image for unsafe or policy‑sensitive visual content using Google Cloud Vision safe‑search detection."""
    client = get_vision_client()
    feature = Feature(type_=Feature_Type.SAFE_SEARCH_DETECTION)
    request = prepare_image_bytes(image_bytes)
    request["features"].append(feature)

    response = client.annotate_image(request)
    return extract_safe_search(response["safe_search_annotation"])
