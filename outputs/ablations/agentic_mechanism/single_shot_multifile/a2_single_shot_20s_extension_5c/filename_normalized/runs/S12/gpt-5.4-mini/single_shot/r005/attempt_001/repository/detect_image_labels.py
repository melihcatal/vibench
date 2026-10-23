import os
from typing import Any, Dict, List

from google.cloud import vision

from vision_client import load_vision_config, open_image_bytes, vision_client
from vision_models import ImageLabel, normalize_label_response, resolve_input_path


def detect_image_labels(image_path: str, max_results: int = 10) -> Dict[str, Any]:
    config = load_vision_config()
    path = resolve_input_path(image_path)
    with open_image_bytes(path) as content:
        image = vision.Image(content=content)
        client = vision_client()
        response = client.label_detection(image=image, max_results=max_results)
    return normalize_label_response(response, image_path=path, provider="google_cloud_vision", kind="labels")
