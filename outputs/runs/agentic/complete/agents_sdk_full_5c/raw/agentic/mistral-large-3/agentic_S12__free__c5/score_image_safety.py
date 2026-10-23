import os
from typing import Dict, List
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageSafetyResponse


def score_image_safety(image_path: str) -> ImageSafetyResponse:
    """Check an image for unsafe or policy-sensitive content using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.safe_search_detection(image=image)
    
    safe_search = response.safe_search_annotation
    
    return ImageSafetyResponse(
        adult=safe_search.adult,
        violence=safe_search.violence,
        racy=safe_search.racy,
        medical=safe_search.medical,
        spoof=safe_search.spoof
    )