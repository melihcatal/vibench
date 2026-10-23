import base64
import os
from typing import Any, Dict, List

from google.cloud import vision

from vision_models import normalize_labels, normalize_text


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def load_image_content(image_path: str) -> bytes:
    with open(image_path, "rb") as handle:
        return handle.read()


def build_image(image_path: str) -> vision.Image:
    return vision.Image(content=load_image_content(image_path))


def labels_from_response(response: Any) -> List[str]:
    return normalize_labels([{"description": item.description} for item in getattr(response, "label_annotations", [])])


def text_from_response(response: Any) -> str:
    annotations = getattr(response, "text_annotations", [])
    if not annotations:
        return ""
    return normalize_text(annotations[0].description)


def safe_search_from_response(response: Any) -> Dict[str, str]:
    safe = getattr(response, "safe_search_annotation", None)
    if safe is None:
        return {"safety": "unknown"}
    return {
        "adult": str(getattr(safe, "adult", "unknown")),
        "medical": str(getattr(safe, "medical", "unknown")),
        "spoof": str(getattr(safe, "spoof", "unknown")),
        "violence": str(getattr(safe, "violence", "unknown")),
        "racy": str(getattr(safe, "racy", "unknown")),
    }
