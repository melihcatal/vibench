from google.cloud import vision
from vision_client import get_google_vision_client
from vision_models import SafetyAnnotation

def score_image_safety(image_path: str) -> list[SafetyAnnotation]:
    """
    Performs safe search detection on an image using Google Cloud Vision API.

    Args:
        image_path: The path to the local image file.

    Returns:
        A list of SafetyAnnotation objects with categories and likelihood ratings.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )
    
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
