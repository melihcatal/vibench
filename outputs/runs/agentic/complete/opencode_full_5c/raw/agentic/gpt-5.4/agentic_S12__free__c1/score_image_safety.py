from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_input,
)
from vision_models import ImageSafetyResult


def score_image_safety(
    image_path: str | None = None, image_uri: str | None = None
) -> dict:
    image_input = load_image_input(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.safe_search_detection(
        image=build_google_vision_image(image_input)
    )
    safe_search = response.safe_search_annotation
    categories = [
        {"name": "adult", "likelihood": int(safe_search.adult)},
        {"name": "medical", "likelihood": int(safe_search.medical)},
        {"name": "spoof", "likelihood": int(safe_search.spoof)},
        {"name": "violence", "likelihood": int(safe_search.violence)},
        {"name": "racy", "likelihood": int(safe_search.racy)},
    ]
    safe = all(item["likelihood"] <= 2 for item in categories)
    return ImageSafetyResult(
        provider="google-cloud-vision", safe=safe, categories=categories
    ).to_dict()
