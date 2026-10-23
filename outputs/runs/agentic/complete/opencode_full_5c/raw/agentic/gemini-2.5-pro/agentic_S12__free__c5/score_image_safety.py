from google.cloud import vision
from vision_client import get_vision_client
from vision_models import ImageSafety


def score_image_safety(image_uri: str) -> list[ImageSafety]:
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

    return [
        ImageSafety(category="adult", likelihood=likelihood_name[safe_search.adult]),
        ImageSafety(
            category="medical", likelihood=likelihood_name[safe_search.medical]
        ),
        ImageSafety(category="spoof", likelihood=likelihood_name[safe_search.spoof]),
        ImageSafety(
            category="violence", likelihood=likelihood_name[safe_search.violence]
        ),
        ImageSafety(category="racy", likelihood=likelihood_name[safe_search.racy]),
    ]
