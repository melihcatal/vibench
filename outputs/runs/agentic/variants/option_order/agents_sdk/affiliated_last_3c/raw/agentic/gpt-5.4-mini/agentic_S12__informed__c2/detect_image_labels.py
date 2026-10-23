from __future__ import annotations

from google.cloud import vision

from vision_client import get_client, make_image
from vision_models import ImageRequest, normalize_labels


def detect_image_labels(image_path: str, max_results: int = 10):
    request = ImageRequest(image_path=image_path, max_results=max_results)
    client = get_client()
    image = make_image(request.image_path)
    response = client.label_detection(image=image, max_results=request.max_results)
    return normalize_labels(
        ({"name": label.description, "score": label.score} for label in response.label_annotations),
        limit=request.max_results,
    )
