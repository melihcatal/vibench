from __future__ import annotations

from typing import Optional

from vision_client import VisionClient
from vision_models import ImageInput, VisionRequest


def describe_image(image_path: str | None = None, image_uri: str | None = None, image_bytes: bytes | None = None) -> str:
    client = VisionClient()
    request = VisionRequest(image=ImageInput(image_path=image_path, image_uri=image_uri, image_bytes=image_bytes), max_results=1)
    response = client.rekognition.detect_labels(
        Image=client.resolve_image_reference(request.image),
        MaxLabels=1,
        MinConfidence=60.0,
    )
    labels = response.get("Labels", [])
    if not labels:
        return "An image with no detected labels."
    top = labels[0]
    return f"An image likely showing {top.get('Name', 'something')} with confidence {top.get('Confidence', 0):.1f}%."
