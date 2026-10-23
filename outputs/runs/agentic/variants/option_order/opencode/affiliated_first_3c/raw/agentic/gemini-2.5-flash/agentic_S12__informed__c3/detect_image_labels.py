import os
from google.cloud import vision


def detect_image_labels(image_content: bytes) -> list[str]:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels
