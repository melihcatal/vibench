from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_vision_client
from document_models import OCRResponse


def extract_text(
    image_path: str, language_hints: Optional[List[str]] = None
) -> OCRResponse:
    """Extract plain text from a scanned document image using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = types.AnnotateImageRequest(
        image=image,
        features=features,
        image_context={"language_hints": language_hints} if language_hints else None,
    )

    response = client.annotate_image(request)
    return OCRResponse.from_vision_response(response)
