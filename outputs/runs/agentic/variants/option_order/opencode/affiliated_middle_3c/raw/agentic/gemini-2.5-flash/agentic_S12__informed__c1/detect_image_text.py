from google.cloud import vision
from vision_client import get_vision_client
from vision_models import (
    ImageDetectionRequest,
    TextDetectionResponse,
    normalize_text_detection_response,
)


def detect_image_text(request: ImageDetectionRequest) -> TextDetectionResponse:
    """
    Detects text appearing inside an image using Google Cloud Vision API.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.text_detection(image=image)
    return normalize_text_detection_response(response)
