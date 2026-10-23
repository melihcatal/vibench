from google.cloud import vision

from vision_client import load_vision_config, require_image_path
from vision_models import VisionSafetyResult


def score_image_safety(image_path: str) -> VisionSafetyResult:
    require_image_path(image_path)
    load_vision_config()
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        image = vision.Image(content=f.read())
    response = client.safe_search_detection(image=image)
    categories = {
        "adult": float(response.safe_search_annotation.adult),
        "violence": float(response.safe_search_annotation.violence),
        "racy": float(response.safe_search_annotation.racy),
        "medical": float(response.safe_search_annotation.medical),
        "spoof": float(response.safe_search_annotation.spoof),
    }
    unsafe = any(v >= 3 for v in categories.values())
    return VisionSafetyResult(unsafe=unsafe, categories=categories)
