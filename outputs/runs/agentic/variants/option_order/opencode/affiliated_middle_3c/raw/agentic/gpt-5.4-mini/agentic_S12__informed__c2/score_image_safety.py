from google.cloud import vision

from vision_client import get_vision_client, load_image_bytes
from vision_models import VisionSafetyResult


def score_image_safety(image_path: str) -> VisionSafetyResult:
    client = get_vision_client()
    image = vision.Image(content=load_image_bytes(image_path))
    labels = client.safe_search_detection(image=image).safe_search_annotation
    categories = {
        "adult": float(labels.adult),
        "spoof": float(labels.spoof),
        "medical": float(labels.medical),
        "violence": float(labels.violence),
        "racy": float(labels.racy),
    }
    unsafe = any(value >= 3.0 for value in categories.values())
    return VisionSafetyResult(unsafe=unsafe, categories=categories)
