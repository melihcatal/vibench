import io
import os
from typing import Union

from google.cloud import vision

from document_client import GoogleCloudClients
from document_models import ExtractedText


def extract_text_from_image(image_bytes: Union[bytes, str]) -> ExtractedText:
    """Extracts plain text from a scanned document image using Google Cloud Vision AI.

    Args:
        image_bytes: The content of the image file as bytes or a GCS URI (gs://...).

    Returns:
        An ExtractedText object containing the full text content.
    """
    client = GoogleCloudClients.get_vision_client()

    if isinstance(image_bytes, str) and image_bytes.startswith("gs://"):
        image = vision.Image(source=vision.ImageSource(image_uri=image_bytes))
    else:
        image = vision.Image(content=image_bytes)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        return ExtractedText(text_content=full_text)
    else:
        return ExtractedText(text_content="")
