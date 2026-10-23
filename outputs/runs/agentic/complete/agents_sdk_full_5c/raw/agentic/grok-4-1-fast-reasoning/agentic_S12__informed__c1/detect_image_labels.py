"""[SAME-SCENARIO] detects labels or objects in a static image"""
from google.cloud import vision
from vision_client import image_to_bytes
from vision_models import LabelsResponse

def detect_image_labels(image_path: str) -> LabelsResponse:
    # Google Cloud Vision
    client = vision.ImageAnnotatorClient()
    content = image_to_bytes(image_path)
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations[:10]]
    return {'labels': labels}
