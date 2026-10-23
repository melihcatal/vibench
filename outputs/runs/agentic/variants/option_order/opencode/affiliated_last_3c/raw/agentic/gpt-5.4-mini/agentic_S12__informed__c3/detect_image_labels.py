from google.cloud import vision

from vision_client import load_vision_config, require_image_path
from vision_models import normalize_labels


def detect_image_labels(image_path: str):
    require_image_path(image_path)
    load_vision_config()
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        image = vision.Image(content=f.read())
    response = client.label_detection(image=image)
    return normalize_labels(response.label_annotations)
