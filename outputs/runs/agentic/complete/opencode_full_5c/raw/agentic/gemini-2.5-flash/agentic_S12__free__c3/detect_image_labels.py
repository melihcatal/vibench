from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import create_vision_image, parse_label_detection_response


def detect_image_labels(image_path_or_bytes):
    """
    Detects labels or objects in a static image using Google Cloud Vision AI.
    Provider: Google Cloud Vision AI
    """
    client = get_vision_client()
    image = create_vision_image(image_path_or_bytes)

    response = client.label_detection(image=image)
    return parse_label_detection_response(response)
