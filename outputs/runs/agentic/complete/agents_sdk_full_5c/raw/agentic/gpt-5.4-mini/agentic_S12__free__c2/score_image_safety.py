from typing import Optional

from google.cloud import vision

from vision_client import get_image_source, get_vision_client
from vision_models import SafetyScoreResult, score_safe_search


def score_image_safety(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> SafetyScoreResult:
    client = get_vision_client()
    content = get_image_source(image_path=image_path, image_bytes=image_bytes)
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    score = score_safe_search(response.safe_search_annotation)
    return SafetyScoreResult(score=score, raw_response=response)
