from google.cloud import vision
import os

def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Google Cloud Vision API."""

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description_parts = [label.description for label in labels[:5]]
        description = "This image likely contains: " + ", ".join(description_parts) + "."
    else:
        description = "Unable to generate a description for this image."

    return description
