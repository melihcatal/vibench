from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageSafety


def score_image_safety(image_uri: str) -> ImageSafety:
    """Checks an image for unsafe content using Google Cloud Vision API."""
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    return ImageSafety(
        adult=likelihood_name[safe.adult],
        spoof=likelihood_name[safe.spoof],
        medical=likelihood_name[safe.medical],
        violence=likelihood_name[safe.violence],
        racy=likelihood_name[safe.racy],
    )
