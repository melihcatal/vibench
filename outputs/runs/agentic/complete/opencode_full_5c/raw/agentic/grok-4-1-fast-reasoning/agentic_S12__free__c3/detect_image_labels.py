from google.cloud import vision_v1 as vision
from vision_client import image_to_bytes
from vision_models import ImageLabels
from typing import List


def detect_image_labels(image_path: str) -> ImageLabels:
    client = vision.ImageAnnotatorClient()
    content = image_to_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:10]]
    return ImageLabels(labels=labels)
