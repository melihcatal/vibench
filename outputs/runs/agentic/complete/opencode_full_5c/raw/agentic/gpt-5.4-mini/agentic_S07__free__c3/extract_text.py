import os

from google.cloud import vision

from document_client import normalize_image_source, vision_client
from document_models import normalize_text


def extract_text(image_source):
    client = vision_client()
    src = normalize_image_source(image_source)
    if "content" in src:
        image = vision.Image(content=src["content"])
    elif "uri" in src:
        image = vision.Image(source=vision.ImageSource(image_uri=src["uri"]))
    else:
        with open(src["path"], "rb") as f:
            image = vision.Image(content=f.read())
    response = client.text_detection(image=image)
    text = response.text_annotations[0].description if response.text_annotations else ""
    return normalize_text(text)
