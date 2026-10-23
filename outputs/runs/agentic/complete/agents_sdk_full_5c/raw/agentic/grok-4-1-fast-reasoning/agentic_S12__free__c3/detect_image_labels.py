import os
from google.cloud import vision
from vision_models import parse_google_labels
from vision_client import load_image

def detect_image_labels(image_path: str) -> list[str]:
    content = load_image(image_path)
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    return parse_google_labels(response)