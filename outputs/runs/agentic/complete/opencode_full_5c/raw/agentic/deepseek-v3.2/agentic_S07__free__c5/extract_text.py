import os
from google.cloud import vision
from document_client import get_vision_client
from document_models import TextExtractionRequest, TextExtractionResponse


def extract_text(request: TextExtractionRequest) -> TextExtractionResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision OCR."""
    client = get_vision_client()

    with open(request.image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        return TextExtractionResponse(
            text=full_text,
            confidence=response.text_annotations[0].confidence
            if hasattr(texts[0], "confidence")
            else 0.9,
            provider="google-cloud-vision",
            raw_response=response,
        )
    else:
        return TextExtractionResponse(
            text="",
            confidence=0.0,
            provider="google-cloud-vision",
            raw_response=response,
        )
