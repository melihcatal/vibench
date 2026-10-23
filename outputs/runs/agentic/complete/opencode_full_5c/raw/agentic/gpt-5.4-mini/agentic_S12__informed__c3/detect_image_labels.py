from typing import Any, Dict

from google.cloud import vision

from vision_client import client, image_input
from vision_models import normalize_label


def detect_image_labels(source: str, max_results: int = 10) -> Dict[str, Any]:
    annotator = client()
    image = image_input(source)
    response = annotator.label_detection(image=image, max_results=max_results)
    return {"labels": [normalize_label(item) for item in response.label_annotations]}
