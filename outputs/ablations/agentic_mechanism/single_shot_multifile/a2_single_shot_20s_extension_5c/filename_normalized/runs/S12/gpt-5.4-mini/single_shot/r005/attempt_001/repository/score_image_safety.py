from typing import Any, Dict

from google.cloud import vision

from vision_client import load_vision_config, open_image_bytes, vision_client
from vision_models import normalize_safety_response, resolve_input_path


def score_image_safety(image_path: str) -> Dict[str, Any]:
    load_vision_config()
    path = resolve_input_path(image_path)
    with open_image_bytes(path) as content:
        image = vision.Image(content=content)
        client = vision_client()
        response = client.safe_search_detection(image=image)
    return normalize_safety_response(response, image_path=path, provider="google_cloud_vision")
