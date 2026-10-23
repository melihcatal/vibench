from __future__ import annotations

from typing import Optional

from google.cloud import vision

from vision_client import DEFAULT_PROVIDER, build_image_source, load_vision_client
from vision_models import VisionResult


MODEL_FAMILY = "google-cloud-vision-web-detection"


def describe_image(path: Optional[str] = None, uri: Optional[str] = None) -> dict:
    client = load_vision_client()
    image, image_meta = build_image_source(path=path, uri=uri)
    response = client.web_detection(image=image)
    web = response.web_detection

    candidates = []
    if getattr(web, "best_guess_labels", None):
        candidates.extend(label.label for label in web.best_guess_labels if label.label)
    if getattr(web, "web_entities", None):
        candidates.extend(entity.description for entity in web.web_entities if entity.description)

    unique = []
    for item in candidates:
        if item not in unique:
            unique.append(item)
    description = ", ".join(unique[:3]) if unique else "Unlabeled image"

    result = VisionResult(
        provider=DEFAULT_PROVIDER,
        model=MODEL_FAMILY,
        image=image_meta,
        description=description,
        raw_response={
            "best_guess_labels": [label.label for label in getattr(web, "best_guess_labels", [])],
            "web_entities": [entity.description for entity in getattr(web, "web_entities", []) if entity.description],
        },
    )
    return result.to_dict()
