from vision_client import get_vision_client
from vision_models import normalize_safe_search_detection_response
from google.cloud import vision

def score_image_safety(image_path: str):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)

    return normalize_safe_search_detection_response(response)
