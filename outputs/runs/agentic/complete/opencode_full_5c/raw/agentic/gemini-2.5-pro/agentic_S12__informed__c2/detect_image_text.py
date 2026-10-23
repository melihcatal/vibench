from vision_client import get_vision_client
from vision_models import TextAnnotation
from google.cloud import vision
from typing import List, Optional


def detect_image_text(image_uri: str) -> Optional[str]:
    """
    Detects text in an image using the Google Cloud Vision API (OCR).

    Args:
        image_uri: The URI of the image (e.g., "gs://..." or "http://...").

    Returns:
        The full detected text as a single string, or None if no text is found.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    if response.text_annotations:
        # The first annotation is the full text block
        return response.text_annotations[0].description

    return None
