from typing import Any, Dict

from vision_client import image_to_base64, post_google_vision


def describe_image(image_bytes: bytes) -> str:
    request_body: Dict[str, Any] = {
        "requests": [
            {
                "image": {"content": image_to_base64(image_bytes)},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 5}],
            }
        ]
    }
    payload = post_google_vision(request_body)
    labels = payload.get("responses", [{}])[0].get("labelAnnotations", [])
    descriptions = [item.get("description", "") for item in labels if item.get("description")]
    return ", ".join(descriptions[:3])
