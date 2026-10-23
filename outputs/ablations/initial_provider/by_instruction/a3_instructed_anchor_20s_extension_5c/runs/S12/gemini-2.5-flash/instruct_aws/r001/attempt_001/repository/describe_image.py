import os
from google.cloud import vision

def describe_image(image_bytes: bytes) -> dict:
    """
    Generates a short visual description for an image using Google Cloud Vision API.

    Args:
        image_bytes: The image content in bytes.

    Returns:
        A dictionary containing the image description.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    
    response = client.label_detection(image=image)
    
    labels = response.label_annotations
    description = ", ".join([label.description for label in labels if label.description])
    
    return {'description': description}
