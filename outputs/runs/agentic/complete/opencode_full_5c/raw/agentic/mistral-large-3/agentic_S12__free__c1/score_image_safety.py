import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import ImageSafetyResponse


def score_image_safety(image_path: str) -> ImageSafetyResponse:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search.adult,
        "spoof": safe_search.spoof,
        "medical": safe_search.medical,
        "violence": safe_search.violence,
        "racy": safe_search.racy,
    }

    return ImageSafetyResponse(
        provider="google_cloud_vision",
        model="safe_search_detection",
        safety_scores=safety_scores,
    )
