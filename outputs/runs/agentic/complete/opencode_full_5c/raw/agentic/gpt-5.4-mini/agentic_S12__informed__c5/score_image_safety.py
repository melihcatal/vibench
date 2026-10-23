from typing import Any, Dict

from vision_client import as_image_payload, rekognition_client
from vision_models import normalize_safety


def score_image_safety(image: Any) -> Dict[str, Any]:
    client = rekognition_client()
    response = client.detect_moderation_labels(Image=as_image_payload(image))
    normalized = normalize_safety(response)
    return {
        "unsafe": len(normalized.moderation_labels) > 0,
        "labels": normalized.moderation_labels,
    }
