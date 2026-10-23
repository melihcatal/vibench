from typing import Any, Dict

from vision_client import as_image_payload, rekognition_client
from vision_models import normalize_text, compact_text


def detect_image_text(image: Any) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_text(Image=as_image_payload(image))
    normalized = normalize_text(response)
    return {
        "text": compact_text(normalized.text_detections),
        "detections": normalized.text_detections,
    }
