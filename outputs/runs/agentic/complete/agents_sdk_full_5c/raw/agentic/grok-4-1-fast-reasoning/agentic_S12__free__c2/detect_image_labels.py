from typing import Dict, Any
from vision_client import vision_client
from vision_models import normalize_labels
from google.cloud import vision_v1 as vision

def detect_image_labels(image_path: str) -> Dict[str, Any]:
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image, max_results=10)
    return normalize_labels(response)
