from __future__ import annotations

from typing import List

from google.cloud import vision

from vision_client import get_vision_client, load_image_content, load_image_uri
from vision_models import OCRTextBlock, normalize_confidence


GOOGLE_VISION_FEATURE = vision.Feature.Type.TEXT_DETECTION


def detect_image_text(image_path: str | None = None, image_uri: str | None = None) -> List[OCRTextBlock]:
    client = get_vision_client()
    image = load_image_uri(image_uri) if image_uri else load_image_content(image_path or "")
    response = client.text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    blocks: List[OCRTextBlock] = []
    for annotation in response.text_annotations[1:]:
        blocks.append(
            OCRTextBlock(
                text=annotation.description,
                confidence=normalize_confidence(getattr(annotation, "confidence", 0.0), 100.0),
                block_type="WORD",
            )
        )
    if not blocks and response.full_text_annotation.text:
        blocks.append(OCRTextBlock(text=response.full_text_annotation.text.strip(), confidence=100.0, block_type="DOCUMENT"))
    return blocks
