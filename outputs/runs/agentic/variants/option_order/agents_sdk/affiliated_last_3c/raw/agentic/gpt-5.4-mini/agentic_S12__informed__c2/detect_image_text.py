from __future__ import annotations

from vision_client import get_client, make_image
from vision_models import ImageRequest, normalize_texts


def detect_image_text(image_path: str, max_results: int = 10):
    request = ImageRequest(image_path=image_path, max_results=max_results)
    client = get_client()
    image = make_image(request.image_path)
    response = client.text_detection(image=image)
    return normalize_texts(
        ({"text": text.description, "score": getattr(text, "confidence", 0.0)} for text in response.text_annotations[1:]),
        limit=request.max_results,
    )
