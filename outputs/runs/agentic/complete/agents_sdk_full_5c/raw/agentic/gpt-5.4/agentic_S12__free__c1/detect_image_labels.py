from __future__ import annotations

from typing import List, Optional

from vision_client import GOOGLE_VISION_PROVIDER, build_google_image, get_google_vision_client, load_image_source
from vision_models import DetectionLabel, normalize_google_labels


PROVIDER = GOOGLE_VISION_PROVIDER


def detect_image_labels(*, image_path: Optional[str] = None, image_uri: Optional[str] = None) -> List[DetectionLabel]:
    client = get_google_vision_client()
    image = build_google_image(load_image_source(image_path=image_path, image_uri=image_uri))
    response = client.annotate_image(
        {
            "image": image,
            "features": [
                {"type_": "LABEL_DETECTION", "max_results": 15},
                {"type_": "OBJECT_LOCALIZATION", "max_results": 15},
            ],
        }
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    return normalize_google_labels(response)
