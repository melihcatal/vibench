from vision_client import get_google_vision_client
from vision_models import ImageSafety
from google.cloud import vision


def score_image_safety(image_uri: str) -> ImageSafety:
    client = get_google_vision_client()
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

    return ImageSafety(
        adult=likelihood_name[safe_search.adult],
        spoof=likelihood_name[safe_search.spoof],
        medical=likelihood_name[safe_search.medical],
        violence=likelihood_name[safe_search.violence],
        racy=likelihood_name[safe_search.racy],
    )
