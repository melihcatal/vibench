import os
from google.cloud import vision
from document_models import TextResponse


def extract_text(image_path: str) -> TextResponse:
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    text = texts[0].description if texts else ""
    return {"text": text}
