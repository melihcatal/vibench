import os
from google.cloud import vision


def detect_image_text(image_content: bytes) -> str:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        # The first text annotation is the overall text detected in the image
        return texts[0].description
    return ""
