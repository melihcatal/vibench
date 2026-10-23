from google.cloud import vision
from .vision_client import image_to_bytes
from .vision_models import Label, VisionLabels

def detect_image_labels(image_path: str) -> VisionLabels:
    client = vision.ImageAnnotatorClient()
    content = image_to_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = []
    for annotation in response.label_annotations or []:
        labels.append({
            'name': annotation.description,
            'confidence': float(annotation.score)
        })
    return {'labels': labels[:10]}