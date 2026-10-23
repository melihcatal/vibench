from google.cloud import vision
from vision_models import SafetyAnnotation

def score_image_safety(image_bytes: bytes) -> list[SafetyAnnotation]:
    """
    Checks an image for unsafe content using Google Cloud Vision API.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)

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

    annotations = [
        SafetyAnnotation(category="adult", likelihood=likelihood_name[safe_search.adult]),
        SafetyAnnotation(category="medical", likelihood=likelihood_name[safe_search.medical]),
        SafetyAnnotation(category="spoof", likelihood=likelihood_name[safe_search.spoof]),
        SafetyAnnotation(category="violence", likelihood=likelihood_name[safe_search.violence]),
        SafetyAnnotation(category="racy", likelihood=likelihood_name[safe_search.racy]),
    ]

    return annotations
