from __future__ import annotations

from typing import Dict, Any

from vision_client import get_aws_rekognition_client
from vision_models import ImageSafetyRequest, normalize_safety_score


def score_image_safety(image_url: str, *, image_path: str | None = None) -> Dict[str, Any]:
    """Check an image for unsafe or policy-sensitive visual content using AWS Rekognition."""
    request = ImageSafetyRequest(image_url=image_url, image_path=image_path)
    client = get_aws_rekognition_client()
    response = client.score_image(request)
    return normalize_safety_score(response)
