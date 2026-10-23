from google.cloud import vision
from vision_client import image_to_bytes
from vision_models import VisionLabels


def detect_image_labels(image_path: str) -> VisionLabels:
    client = vision.ImageAnnotatorClient()
    image_bytes = image_to_bytes(image_path)
    image = vision.Image(content=image_bytes)
    response = client.label_detection(image=image)
    labels = [
        label.description
        for label in response.label_annotations[:10]
        if label.description
    ]
    return VisionLabels(labels=labels)
