from vision_client import get_vision_client
from vision_models import SafeSearchAnnotation
from google.cloud import vision
from typing import Optional


def score_image_safety(image_uri: str) -> Optional[SafeSearchAnnotation]:
    """
    Performs safe search detection on an image using Google Cloud Vision API.

    Args:
        image_uri: The URI of the image (e.g., "gs://..." or "http://...").

    Returns:
        A SafeSearchAnnotation object with likelihood scores.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    safe = response.safe_search_annotation

    # The response enums are integers, convert them to string representations
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    return SafeSearchAnnotation(
        adult=likelihood_name[safe.adult],
        spoof=likelihood_name[safe.spoof],
        medical=likelihood_name[safe.medical],
        violence=likelihood_name[safe.violence],
        racy=likelihood_name[safe.racy],
    )
