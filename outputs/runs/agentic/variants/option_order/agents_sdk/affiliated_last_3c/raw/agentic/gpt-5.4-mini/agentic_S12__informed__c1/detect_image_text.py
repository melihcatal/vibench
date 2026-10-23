from __future__ import annotations

from typing import List

from vision_client import VisionClient
from vision_models import ImageInput, VisionTextResult, VisionRequest


def detect_image_text(image_path: str | None = None, image_uri: str | None = None, image_bytes: bytes | None = None) -> List[VisionTextResult]:
    client = VisionClient()
    request = VisionRequest(image=ImageInput(image_path=image_path, image_uri=image_uri, image_bytes=image_bytes), max_results=10)
    response = client.rekognition.detect_text(Image=client.resolve_image_reference(request.image))
    results: List[VisionTextResult] = []
    for detection in response.get("TextDetections", []):
        if detection.get("Type") == "LINE" or detection.get("DetectedText"):
            results.append(VisionTextResult(text=str(detection.get("DetectedText", "")), confidence=detection.get("Confidence")))
    return results
