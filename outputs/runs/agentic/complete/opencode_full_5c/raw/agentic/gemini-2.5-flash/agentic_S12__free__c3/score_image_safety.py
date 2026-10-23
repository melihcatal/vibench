from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import create_vision_image, parse_safe_search_detection_response


def score_image_safety(image_path_or_bytes):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.
    Provider: Google Cloud Vision AI
    """
    client = get_vision_client()
    image = create_vision_image(image_path_or_bytes)

    response = client.safe_search_detection(image=image)
    return parse_safe_search_detection_response(response)
