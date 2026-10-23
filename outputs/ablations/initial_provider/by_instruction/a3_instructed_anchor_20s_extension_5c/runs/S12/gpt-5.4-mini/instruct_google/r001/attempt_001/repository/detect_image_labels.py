from google.cloud import vision

from vision_client import vision_client
from vision_models import normalize_labels


def detect_image_labels(image_path: str):
    client = vision_client()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return normalize_labels([label.description for label in response.label_annotations])
