from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import create_vision_image, parse_text_detection_response


def detect_image_text(image_path_or_bytes):
    """
    Detects text appearing inside an image using Google Cloud Vision AI.
    Provider: Google Cloud Vision AI
    """
    client = get_vision_client()
    image = create_vision_image(image_path_or_bytes)

    response = client.text_detection(image=image)
    texts = parse_text_detection_response(response)

    if texts:
        # The first element in texts is usually the full text detected
        return texts[0]
    return "No text detected in the image."
