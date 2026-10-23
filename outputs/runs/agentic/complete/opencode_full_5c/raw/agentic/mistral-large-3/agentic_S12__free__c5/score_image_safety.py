import io
from typing import List
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageSafetyRating, normalize_safety_ratings


def score_image_safety(image_path: str) -> List[ImageSafetyRating]:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API."""
    client = get_vision_client()

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = {"content": content}
    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    safe_search = response.safe_search_annotation
    safety_ratings = [
        {"category": "adult", "probability": safe_search.adult.name},
        {"category": "spoof", "probability": safe_search.spoof.name},
        {"category": "medical", "probability": safe_search.medical.name},
        {"category": "violence", "probability": safe_search.violence.name},
        {"category": "racy", "probability": safe_search.racy.name},
    ]

    return normalize_safety_ratings(safety_ratings)
