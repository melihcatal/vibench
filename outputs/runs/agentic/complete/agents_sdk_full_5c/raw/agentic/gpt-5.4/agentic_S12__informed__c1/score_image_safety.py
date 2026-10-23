from __future__ import annotations

from vision_client import build_gcv_image, get_google_vision_client
from vision_models import ImageSafetyResult, is_safe_search_flagged, normalize_safe_search


PROVIDER = "google-cloud-vision"


def score_image_safety(image_path: str) -> ImageSafetyResult:
    client = get_google_vision_client()
    image = build_gcv_image(image_path)
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    safe_search = normalize_safe_search(response.safe_search_annotation)
    return ImageSafetyResult(
        provider=PROVIDER,
        safe_search=safe_search,
        flagged=is_safe_search_flagged(safe_search),
    )
