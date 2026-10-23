from __future__ import annotations

from vision_client import (
    build_google_vision_image,
    get_google_vision_client,
    load_image_source,
)
from vision_models import ImageTextDetectionResult, compact_text, normalize_text_blocks


def detect_image_text(
    image_path: str | None = None,
    image_uri: str | None = None,
    image_bytes: bytes | None = None,
) -> dict:
    client = get_google_vision_client()
    source = load_image_source(
        image_path=image_path, image_uri=image_uri, image_bytes=image_bytes
    )
    image = build_google_vision_image(source)
    response = client.text_detection(image=image)
    blocks = normalize_text_blocks(
        [
            {
                "text": annotation.description,
                "kind": "TEXT",
                "confidence": getattr(annotation, "confidence", 0.0) * 100.0,
            }
            for annotation in response.text_annotations
        ]
    )
    return ImageTextDetectionResult(text=compact_text(blocks), blocks=blocks).to_dict()
