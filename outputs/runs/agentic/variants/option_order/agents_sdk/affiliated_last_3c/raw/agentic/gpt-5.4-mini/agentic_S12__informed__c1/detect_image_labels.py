from __future__ import annotations

from typing import List

from vision_client import VisionClient
from vision_models import ImageInput, VisionItem, VisionRequest, normalize_items


def detect_image_labels(image_path: str | None = None, image_uri: str | None = None, image_bytes: bytes | None = None) -> List[VisionItem]:
    client = VisionClient()
    request = VisionRequest(image=ImageInput(image_path=image_path, image_uri=image_uri, image_bytes=image_bytes), max_results=10)
    response = client.rekognition.detect_labels(**{
        "Image": client.resolve_image_reference(request.image),
        "MaxLabels": request.max_results,
        "MinConfidence": 50.0,
    })
    return normalize_items(
        ({"name": label.get("Name"), "confidence": label.get("Confidence"), "bounding_box": label.get("Instances", [{}])[0].get("BoundingBox") if label.get("Instances") else None} for label in response.get("Labels", []))
    )
