from google.cloud import vision
from vision_client import get_vision_client
from vision_models import SafetyRating
from typing import List


def score_image_safety(image_uri: str) -> List[SafetyRating]:
    """Scores the image for unsafe content."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    ratings = [
        SafetyRating(category="adult", likelihood=likelihood_name[safe_search.adult]),
        SafetyRating(category="spoof", likelihood=likelihood_name[safe_search.spoof]),
        SafetyRating(
            category="medical", likelihood=likelihood_name[safe_search.medical]
        ),
        SafetyRating(
            category="violence", likelihood=likelihood_name[safe_search.violence]
        ),
        SafetyRating(category="racy", likelihood=likelihood_name[safe_search.racy]),
    ]
    return ratings
