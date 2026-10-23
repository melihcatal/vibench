from google.cloud import vision
from vision_client import image_to_bytes
from vision_models import ImageLabels

def detect_image_labels(image_path: str) -> ImageLabels:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_to_bytes(image_path))
    response = client.label_detection(image=image)
    labels = [
        {'name': label.description, 'confidence': label.score}
        for label in response.label_annotations
    ]
    return {'labels': labels}