from __future__ import annotations

from typing import Optional

from vision_client import (
    build_image_source,
    get_google_vision_client,
    image_source_to_google_image,
)
from vision_models import (
    ImageTextResult,
    OCRTextBlock,
    normalize_score,
    text_result_dict,
)


def detect_image_text(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    image = build_image_source(image_path=image_path, image_uri=image_uri)
    client = get_google_vision_client()
    response = client.text_detection(image=image_source_to_google_image(image))
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotations = list(response.text_annotations)
    full_text = annotations[0].description if annotations else ""
    blocks = [
        OCRTextBlock(
            text=annotation.description,
            score=normalize_score(annotation.confidence or 0.0),
        )
        for annotation in annotations[1:]
    ]
    result = ImageTextResult(
        provider="google-cloud-vision", text_blocks=blocks, full_text=full_text
    )
    return text_result_dict(result)
