from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import SafetyRatingResponse


def score_image_safety(image_path: str) -> SafetyRatingResponse:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    return SafetyRatingResponse(
        adult=safe_search.adult,
        violence=safe_search.violence,
        racy=safe_search.racy,
        medical=safe_search.medical,
        spoof=safe_search.spoof,
    )
