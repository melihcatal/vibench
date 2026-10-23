from typing import Any, Dict

from vision_client import VisionClient
from vision_models import ImageAnalysisRequest, normalize_aws_rekognition_labels


def detect_image_labels(image_path: str) -> Dict[str, Any]:
    client = VisionClient()
    request = ImageAnalysisRequest(image_path=image_path)
    payload = client.detect_labels(request)
    normalized = normalize_aws_rekognition_labels(payload)
    return {"provider": normalized.provider, "request_type": normalized.request_type, "items": normalized.items, "raw": normalized.raw}
