import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import List, Dict
from .vision_client import get_vision_client
from .vision_models import TextDetectionResponse


def detect_image_text(image_path: str) -> TextDetectionResponse:
    """Detects text appearing inside an image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_text = texts[0].description if texts else ""
    text_annotations = []
    for text in texts[1:]:
        text_annotations.append(
            {
                "description": text.description,
                "bounding_poly": {
                    "vertices": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in text.bounding_poly.vertices
                    ]
                },
            }
        )

    return TextDetectionResponse(
        provider="google_cloud_vision",
        model="text_detection",
        detected_text=detected_text,
        text_annotations=text_annotations,
    )
