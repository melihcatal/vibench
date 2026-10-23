import os
from typing import Optional
import base64
from google.cloud import vision
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import OCRResponse, TextExtractionRequest


def extract_text(request: TextExtractionRequest) -> OCRResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision API."""

    client = get_vision_client()

    if request.image_path:
        with open(request.image_path, "rb") as image_file:
            content = image_file.read()
    elif request.image_base64:
        content = base64.b64decode(request.image_base64)
    else:
        raise ValueError("Either image_path or image_base64 must be provided")

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        confidence = texts[0].confidence if hasattr(texts[0], "confidence") else 0.0
    else:
        full_text = ""
        confidence = 0.0

    return OCRResponse(
        text=full_text,
        confidence=confidence,
        provider="google_cloud_vision",
        model="text_detection",
        raw_response=response,
    )
