# describe_image.py
import os
from google.cloud import vision


def describe_image(image_path):
    """Generate a short visual description for an image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.annotate_image(
        {
            "image": {"content": content},
            "features": [{"type_": vision.Feature.Type.DESCRIPTOR_TYPE}],
        }
    )
    if response.full_text_annotation:
        return response.full_text_annotation.text.strip()
    return "No description available."
