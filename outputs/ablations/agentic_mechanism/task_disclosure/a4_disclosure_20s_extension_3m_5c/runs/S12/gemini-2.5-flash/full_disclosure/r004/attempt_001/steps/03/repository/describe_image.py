import os
from google.cloud import vision_v1p3beta1 as vision

def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A string describing the image.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if not labels:
        return "No clear description could be generated for the image."

    description_parts = [label.description for label in labels]
    return "The image likely depicts: " + ", ".join(description_parts) + "."

