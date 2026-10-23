from __future__ import annotations

from typing import Dict, Any

from vision_client import VisionClientFactory, build_vision_image, GOOGLE_VISION_MODEL, GOOGLE_VISION_PROVIDER
from vision_models import ImageSource, TextBlock, VisionResult, normalize_confidence


def detect_image_text(source: ImageSource) -> Dict[str, Any]:
    client = VisionClientFactory.create_image_annotator_client()
    image = build_vision_image(source)
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    text_blocks = []
    for idx, annotation in enumerate(annotations):
        if idx == 0:
            continue
        text_blocks.append(
            TextBlock(
                text=annotation.description,
                confidence=normalize_confidence(1.0),
                language=None,
            )
        )
    result = VisionResult(
        provider=GOOGLE_VISION_PROVIDER,
        model=GOOGLE_VISION_MODEL,
        text_blocks=text_blocks,
        raw_response={"full_text": annotations[0].description if annotations else ""},
    )
    return result.to_dict()
