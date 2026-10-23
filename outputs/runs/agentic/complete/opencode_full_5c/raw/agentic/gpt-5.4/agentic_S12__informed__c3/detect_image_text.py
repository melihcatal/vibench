from __future__ import annotations

from typing import Optional

from vision_client import (
    GOOGLE_VISION_PROVIDER,
    build_google_vision_image,
    get_google_vision_client,
)
from vision_models import TextDetectionResult, normalize_text_annotations


def detect_image_text(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    client = get_google_vision_client()
    image = build_google_vision_image(image_path=image_path, image_uri=image_uri)
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    full_text = (
        response.full_text_annotation.text if response.full_text_annotation else ""
    )
    result = TextDetectionResult(
        provider=GOOGLE_VISION_PROVIDER,
        text=full_text,
        annotations=normalize_text_annotations(response.text_annotations),
        raw_response={"text_annotation_count": len(response.text_annotations)},
    )
    return result.to_dict()
