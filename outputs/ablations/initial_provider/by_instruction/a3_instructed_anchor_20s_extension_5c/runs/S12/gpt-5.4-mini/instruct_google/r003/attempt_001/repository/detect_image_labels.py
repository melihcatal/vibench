from typing import Any, Dict, List

from vision_client import image_to_base64, post_google_vision
from vision_models import normalize_label_annotations


def detect_image_labels(image_bytes: bytes, max_results: int = 10) -> List[str]:
    request_body: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": image_to_base64(image_bytes)},
                "features": [{"type": "LABEL_DETECTION", "maxResults": max_results}],
            }
        ]
    }
    payload = post_google_vision(request_body)
    annotations = payload.get("responses", [{}])[0].get("labelAnnotations", [])
    return normalize_label_annotations(annotations)
