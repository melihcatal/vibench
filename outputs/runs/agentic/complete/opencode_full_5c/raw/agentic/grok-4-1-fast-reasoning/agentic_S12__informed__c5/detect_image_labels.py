from vision_client import load_image_bytes, get_google_vision_client
from vision_models import parse_google_labels
from google.cloud import vision


def detect_image_labels(image_path: str) -> dict:
    image_bytes = load_image_bytes(image_path)
    client = get_google_vision_client()
    image = vision.Image(content=image_bytes)
    response = client.label_detection(image=image)
    return parse_google_labels(response)
