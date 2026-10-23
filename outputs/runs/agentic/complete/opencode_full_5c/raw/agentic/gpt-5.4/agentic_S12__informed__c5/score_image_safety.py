from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_source,
)
from vision_models import ImageSafetyResult


LIKELIHOOD_SCORES = {
    0: 0.0,
    1: 5.0,
    2: 20.0,
    3: 45.0,
    4: 75.0,
    5: 95.0,
}


def score_image_safety(
    image_path: str | None = None,
    image_uri: str | None = None,
    image_bytes: bytes | None = None,
) -> dict:
    client = get_google_vision_client()
    source = load_image_source(
        image_path=image_path, image_uri=image_uri, image_bytes=image_bytes
    )
    image = build_google_vision_image(source)
    response = client.safe_search_detection(image=image)
    annotation = response.safe_search_annotation
    categories = [
        {
            "name": "adult",
            "likelihood": LIKELIHOOD_SCORES.get(int(annotation.adult), 0.0),
        },
        {
            "name": "spoof",
            "likelihood": LIKELIHOOD_SCORES.get(int(annotation.spoof), 0.0),
        },
        {
            "name": "medical",
            "likelihood": LIKELIHOOD_SCORES.get(int(annotation.medical), 0.0),
        },
        {
            "name": "violence",
            "likelihood": LIKELIHOOD_SCORES.get(int(annotation.violence), 0.0),
        },
        {
            "name": "racy",
            "likelihood": LIKELIHOOD_SCORES.get(int(annotation.racy), 0.0),
        },
    ]
    safe = all(item["likelihood"] < 75.0 for item in categories)
    return ImageSafetyResult(safe=safe, categories=categories).to_dict()
