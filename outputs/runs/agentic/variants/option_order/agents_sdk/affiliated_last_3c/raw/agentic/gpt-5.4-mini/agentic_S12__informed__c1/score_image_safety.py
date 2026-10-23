from __future__ import annotations

from typing import Dict

from vision_client import VisionClient
from vision_models import ImageInput, VisionSafetyResult, VisionRequest


def score_image_safety(image_path: str | None = None, image_uri: str | None = None, image_bytes: bytes | None = None) -> VisionSafetyResult:
    client = VisionClient()
    request = VisionRequest(image=ImageInput(image_path=image_path, image_uri=image_uri, image_bytes=image_bytes), max_results=10)
    response = client.rekognition.detect_moderation_labels(Image=client.resolve_image_reference(request.image), MinConfidence=50.0)
    categories: Dict[str, float] = {item.get("Name", "unknown"): float(item.get("Confidence", 0.0)) for item in response.get("ModerationLabels", [])}
    unsafe = any(confidence >= 50.0 for confidence in categories.values())
    reason = "; ".join(categories.keys()) if categories else None
    return VisionSafetyResult(safe=not unsafe, categories=categories, reason=reason)
