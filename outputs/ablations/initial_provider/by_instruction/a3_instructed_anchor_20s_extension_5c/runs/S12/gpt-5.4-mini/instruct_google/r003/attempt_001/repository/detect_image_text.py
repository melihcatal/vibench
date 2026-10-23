from typing import Any, Dict

from vision_client import image_to_base64, post_google_vision
from vision_models import normalize_text_annotations


def detect_image_text(image_bytes: bytes) -> str:
    request_body: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": image_to_base64(image_bytes)},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 1}],
            }
        ]
    }
    payload = post_google_vision(request_body)
    annotations = payload.get("responses", [{}])[0].get("textAnnotations", [])
    return normalize_text_annotations(annotations)
