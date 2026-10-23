from typing import Any, Dict

from google.cloud import vision

from vision_client import client, image_input
from vision_models import normalize_text


def detect_image_text(source: str) -> Dict[str, Any]:
    annotator = client()
    image = image_input(source)
    response = annotator.text_detection(image=image)
    return {"text": [normalize_text(item) for item in response.text_annotations]}
