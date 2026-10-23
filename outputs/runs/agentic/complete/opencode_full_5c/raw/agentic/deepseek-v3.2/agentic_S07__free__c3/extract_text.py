import os
from typing import Optional
import requests
from document_client import get_google_vision_client
from document_models import TextExtractionRequest, TextExtractionResponse


def extract_text(
    image_path: str, language_hints: Optional[list] = None
) -> TextExtractionResponse:
    """
    Extract plain text from a scanned document image using Google Cloud Vision API.
    """
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = client.image(content=content)

    if language_hints:
        image_context = {"language_hints": language_hints}
        response = image.detect_document_text(image_context=image_context)
    else:
        response = image.detect_document_text()

    full_text = (
        response.full_text_annotation.text if response.full_text_annotation else ""
    )

    return TextExtractionResponse(
        text=full_text,
        confidence=response.full_text_annotation.confidence
        if response.full_text_annotation
        else 0.0,
        provider="google_vision",
        raw_response=response,
    )
