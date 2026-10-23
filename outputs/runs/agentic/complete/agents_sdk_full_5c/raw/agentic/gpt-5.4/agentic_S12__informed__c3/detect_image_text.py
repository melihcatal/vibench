from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import build_vision_image, get_google_vision_client
from vision_models import OCRTextBlock


GOOGLE_VISION_FEATURE = vision.Feature.Type.TEXT_DETECTION


def detect_image_text(image_path: str) -> List[OCRTextBlock]:
    client = get_google_vision_client()
    image = build_vision_image(image_path)
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    blocks: List[OCRTextBlock] = []
    for annotation in response.text_annotations[1:]:
        blocks.append(
            OCRTextBlock(
                text=annotation.description,
                confidence=None,
                block_type="text_annotation",
            )
        )
    if not blocks and response.text_annotations:
        blocks.append(
            OCRTextBlock(
                text=response.text_annotations[0].description,
                confidence=None,
                block_type="full_text",
            )
        )
    return blocks
