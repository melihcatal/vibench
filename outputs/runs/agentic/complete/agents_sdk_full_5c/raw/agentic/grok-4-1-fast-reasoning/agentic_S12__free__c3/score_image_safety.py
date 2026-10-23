import os
from google.cloud import vision
from vision_client import load_image
from vision_models import parse_safety

def score_image_safety(image_path: str) -> dict[str, str]:
    content = load_image(image_path)
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    return parse_safety(response)