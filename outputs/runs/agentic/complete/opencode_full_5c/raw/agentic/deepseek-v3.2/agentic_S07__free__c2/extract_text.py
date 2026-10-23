import os
import base64
from google.cloud import vision
from typing import Optional, List


def extract_text_from_image(
    image_path: str, language_hints: Optional[List[str]] = None
) -> str:
    """
    Extract plain text from a scanned document image using Google Cloud Vision OCR.

    Args:
        image_path: Path to the image file
        language_hints: Optional list of language hints for OCR (e.g., ['en', 'es'])

    Returns:
        Extracted text as a string
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    image_context = vision.ImageContext()
    if language_hints:
        image_context.language_hints = language_hints

    response = client.text_detection(image=image, image_context=image_context)

    if response.error.message:
        raise Exception(f"Google Cloud Vision error: {response.error.message}")

    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""


def extract_text_from_bytes(
    image_bytes: bytes, language_hints: Optional[List[str]] = None
) -> str:
    """
    Extract plain text from image bytes using Google Cloud Vision OCR.

    Args:
        image_bytes: Raw image bytes
        language_hints: Optional list of language hints for OCR

    Returns:
        Extracted text as a string
    """
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_bytes)

    image_context = vision.ImageContext()
    if language_hints:
        image_context.language_hints = language_hints

    response = client.text_detection(image=image, image_context=image_context)

    if response.error.message:
        raise Exception(f"Google Cloud Vision error: {response.error.message}")

    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""
