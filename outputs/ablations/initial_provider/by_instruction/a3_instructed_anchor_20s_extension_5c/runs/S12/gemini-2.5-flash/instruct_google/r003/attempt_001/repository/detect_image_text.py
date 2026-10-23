from vision_client import get_vision_client
from vision_models import normalize_text_detection_response
from google.cloud import vision

def detect_image_text(image_path: str):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    return normalize_text_detection_response(response)
