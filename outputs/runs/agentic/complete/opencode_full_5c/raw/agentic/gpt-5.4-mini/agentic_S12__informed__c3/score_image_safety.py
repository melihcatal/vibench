from typing import Any, Dict

from google.cloud import vision

from vision_client import client, image_input
from vision_models import normalize_safety


def score_image_safety(source: str) -> Dict[str, Any]:
    annotator = client()
    image = image_input(source)
    response = annotator.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    findings = [
        normalize_safety("adult", safe.adult),
        normalize_safety("spoof", safe.spoof),
        normalize_safety("medical", safe.medical),
        normalize_safety("violence", safe.violence),
        normalize_safety("racy", safe.racy),
    ]
    return {"findings": findings}
