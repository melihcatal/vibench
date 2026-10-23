from typing import Dict, Any
from vision_client import vision_client
from vision_models import normalize_text
from google.cloud import vision_v1 as vision

def detect_image_text(image_path: str) -> Dict[str, Any]:
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.document_text_detection(image=image)
    return normalize_text(response)
