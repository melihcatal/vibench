import os
from google.cloud import vision
from document_client import get_google_vision_client
from typing import List

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts plain text from a document image using Google Cloud Vision API.

    Args:
        image_path: The local path to the image file.

    Returns:
        A string containing the extracted text.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            f'{response.error.message}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'
        )

    if response.text_annotations:
        return response.text_annotations[0].description
    return ""
