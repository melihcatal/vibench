from google.cloud import vision
from vision_client import get_vision_client
from vision_models import (
    ImageDetectionRequest,
    LabelDetectionResponse,
    normalize_label_detection_response,
)


def detect_image_labels(request: ImageDetectionRequest) -> LabelDetectionResponse:
    """
    Detects labels or objects in a static image using Google Cloud Vision API.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    response = client.label_detection(image=image)
    return normalize_label_detection_response(response)
