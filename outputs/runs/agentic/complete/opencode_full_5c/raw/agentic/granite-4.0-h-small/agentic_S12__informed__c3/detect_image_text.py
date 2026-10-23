import os
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Detect embedded text in an image using Google Cloud Vision OCR.

    Args:
        image_path: Path to the input image file.

    Returns:
        List of extracted text strings.
    """
    client = VisionClient(service="google-cloud-vision")
    response = client.annotate_image(image_path, features=["TEXT_DETECTION"])
    texts = response.get("text", "")
    # Return list of lines
    lines = texts.split("\n") if texts else []
    return [line.strip() for line in lines if line.strip()]
