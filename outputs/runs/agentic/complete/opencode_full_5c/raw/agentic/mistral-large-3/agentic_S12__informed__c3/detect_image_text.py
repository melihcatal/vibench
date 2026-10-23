from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import TextDetectionResponse


def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Detects text in a static image using Google Cloud Vision."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return TextDetectionResponse(
        text=texts[0].description if texts else "",
        bounding_boxes=[
            {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in text.bounding_poly.vertices
                ],
                "description": text.description,
            }
            for text in texts[1:]
        ]
        if len(texts) > 1
        else [],
    )
