import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import LabelDetectionResponse

def detect_image_labels(image_path: str) -> LabelDetectionResponse:
    """Detects labels in a static image using Google Cloud Vision API."""
    client = get_vision_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision_v1.Image(content=content)
    response = client.label_detection(image=image)
    
    return LabelDetectionResponse(
        provider="google-cloud-vision",
        labels=[label.description for label in response.label_annotations],
        confidence=[label.score for label in response.label_annotations]
    )