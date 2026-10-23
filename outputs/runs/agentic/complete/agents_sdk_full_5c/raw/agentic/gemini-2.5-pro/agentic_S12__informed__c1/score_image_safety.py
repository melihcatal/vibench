from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import SafetyAnnotation


def score_safety(image_uri: str) -> list[SafetyAnnotation]:
    """Scores an image for safe search categories using Google Cloud Vision."""
    client = get_google_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    safe_search = response.safe_search_annotation
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    annotations = [
        SafetyAnnotation(category="adult", likelihood=likelihood_name[safe_search.adult]),
        SafetyAnnotation(
            category="medical", likelihood=likelihood_name[safe_search.medical]
        ),
        SafetyAnnotation(category="spoof", likelihood=likelihood_name[safe_search.spoof]),
        SafetyAnnotation(
            category="violence", likelihood=likelihood_name[safe_search.violence]
        ),
        SafetyAnnotation(category="racy", likelihood=likelihood_name[safe_search.racy]),
    ]
    return annotations
