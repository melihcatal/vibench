from typing import Any, Dict

from vision_client import image_to_base64, post_google_vision
from vision_models import normalize_safe_search


def score_image_safety(image_bytes: bytes) -> Dict[str, Any]:
    request_body: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": image_to_base64(image_bytes)},
                "features": [{"type": "SAFE_SEARCH_DETECTION", "maxResults": 1}],
            }
        ]
    }
    payload = post_google_vision(request_body)
    result = payload.get("responses", [{}])[0].get("safeSearchAnnotation", {})
    return normalize_safe_search(result)
