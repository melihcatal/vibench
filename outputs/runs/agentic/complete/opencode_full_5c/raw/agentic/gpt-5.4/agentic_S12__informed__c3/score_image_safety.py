from __future__ import annotations

from typing import Optional

from google.cloud.vision_v1.types import Likelihood

from vision_client import (
    GOOGLE_VISION_PROVIDER,
    build_google_vision_image,
    get_google_vision_client,
)
from vision_models import ImageSafetyResult


def score_image_safety(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    client = get_google_vision_client()
    image = build_google_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.safe_search_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotation = response.safe_search_annotation
    categories = [
        {"category": "adult", "likelihood": Likelihood(annotation.adult).name},
        {"category": "spoof", "likelihood": Likelihood(annotation.spoof).name},
        {"category": "medical", "likelihood": Likelihood(annotation.medical).name},
        {"category": "violence", "likelihood": Likelihood(annotation.violence).name},
        {"category": "racy", "likelihood": Likelihood(annotation.racy).name},
    ]
    blocked = any(
        item["likelihood"] in {"LIKELY", "VERY_LIKELY"}
        for item in categories
        if item["category"] in {"adult", "violence", "racy"}
    )
    result = ImageSafetyResult(
        provider=GOOGLE_VISION_PROVIDER,
        categories=categories,
        blocked=blocked,
        raw_response={"safe_search_present": annotation is not None},
    )
    return result.to_dict()
