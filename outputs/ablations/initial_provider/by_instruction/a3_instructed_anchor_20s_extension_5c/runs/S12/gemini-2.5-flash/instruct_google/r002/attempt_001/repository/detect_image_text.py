from vision_client import get_vision_client
from vision_models import *
from google.cloud import vision

def detect_image_text(image_path):
    client = get_vision_client()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is usually the aggregate of all text found
        return texts[0].description
    else:
        return "No text found in the image."
