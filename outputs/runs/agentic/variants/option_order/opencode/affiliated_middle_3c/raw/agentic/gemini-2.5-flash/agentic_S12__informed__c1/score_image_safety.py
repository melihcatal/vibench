from google.cloud import vision
from vision_client import get_vision_client
from vision_models import (
    ImageDetectionRequest,
    SafeSearchDetectionResponse,
    normalize_safe_search_detection_response,
)


def score_image_safety(request: ImageDetectionRequest) -> SafeSearchDetectionResponse:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API Safe Search.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.safe_search_detection(image=image)
    return normalize_safe_search_detection_response(response)
