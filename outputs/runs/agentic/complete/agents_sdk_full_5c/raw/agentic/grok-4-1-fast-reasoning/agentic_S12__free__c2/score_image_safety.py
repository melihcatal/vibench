from typing import Dict, Any
from vision_client import vision_client
from vision_models import normalize_safety
from google.cloud import vision_v1 as vision

def score_image_safety(image_path: str) -> Dict[str, Any]:
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.safe_search_detection(image=image)
    return normalize_safety(response)
