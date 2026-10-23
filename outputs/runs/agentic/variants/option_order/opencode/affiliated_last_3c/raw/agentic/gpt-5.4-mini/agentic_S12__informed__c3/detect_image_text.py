from google.cloud import vision

from vision_client import load_vision_config, require_image_path
from vision_models import normalize_text


def detect_image_text(image_path: str):
    require_image_path(image_path)
    load_vision_config()
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        image = vision.Image(content=f.read())
    response = client.text_detection(image=image)
    return normalize_text(response.text_annotations)
