from google.cloud import vision
from vision_client import load_image_bytes
from vision_models import VisionLabels

def detect_image_labels(image_path: str) -> VisionLabels:
    client = vision.ImageAnnotatorClient()
    content = load_image_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    scores = [label.score for label in response.label_annotations]
    return VisionLabels(labels=labels, confidence_scores=scores)