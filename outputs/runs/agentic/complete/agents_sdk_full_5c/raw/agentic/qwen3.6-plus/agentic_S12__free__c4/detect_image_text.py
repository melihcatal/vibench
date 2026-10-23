"""
Detects text appearing inside an image using Google Cloud Vision API.
Provider: Google Cloud Vision (google-cloud-vision)
Endpoint: vision.googleapis.com
Model: Google Cloud Vision Text Detection (OCR) v1
"""

from __future__ import annotations

import os
from typing import Optional

from vision_client import (
    build_annotate_request,
    get_vision_client,
    load_image_from_path,
    load_image_from_url,
)
from vision_models import DetectedText, get_text_detection_feature, get_document_text_detection_feature


def detect_text(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    language_hints: Optional[list[str]] = None,
    use_dense_ocr: bool = False,
) -> list[DetectedText]:
    """
    Detect text appearing inside an image using Google Cloud Vision API OCR.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI (http/https or gs://) for the image.
        language_hints: Optional BCP-47 language codes to improve accuracy.
        use_dense_ocr: Whether to use DOCUMENT_TEXT_DETECTION for dense text.

    Returns:
        List of DetectedText objects with text content, confidence, and bounding box.

    Raises:
        ValueError: If neither image_path nor image_uri is provided.
    """
    if not image_path and not image_uri:
        raise ValueError("Either image_path or image_uri must be provided")

    client = get_vision_client()

    if image_path:
        image = load_image_from_path(image_path)
        source = image_path
    else:
        image = load_image_from_url(image_uri)
        source = image_uri

    if use_dense_ocr:
        features = [get_document_text_detection_feature()]
    else:
        features = [get_text_detection_feature()]

    request = build_annotate_request(image, features, language_hints=language_hints)
    response = client.annotate_image(request)

    texts = []
    for entity in response.text_annotations:
        texts.append(DetectedText.from_entity(entity))

    return texts


def extract_full_text(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    language_hints: Optional[list[str]] = None,
    use_dense_ocr: bool = False,
) -> str:
    """
    Extract the complete text content from an image as a single string.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI for the image.
        language_hints: Optional BCP-47 language codes.
        use_dense_ocr: Whether to use dense document OCR.

    Returns:
        Full text content extracted from the image.
    """
    texts = detect_text(
        image_path=image_path,
        image_uri=image_uri,
        language_hints=language_hints,
        use_dense_ocr=use_dense_ocr,
    )

    if texts:
        return texts[0].text
    return ""


def detect_text_with_structure(
    image_path: Optional[str] = None,
    image_uri: Optional[str] = None,
    language_hints: Optional[list[str]] = None,
) -> dict:
    """
    Detect text with structural information (pages, blocks, paragraphs, words).

    Uses DOCUMENT_TEXT_DETECTION for rich OCR output.

    Args:
        image_path: Local path to the image file.
        image_uri: Public URI for the image.
        language_hints: Optional BCP-47 language codes.

    Returns:
        Dictionary with full text, pages, blocks, paragraphs, and words.
    """
    if not image_path and not image_uri:
        raise ValueError("Either image_path or image_uri must be provided")

    client = get_vision_client()

    if image_path:
        image = load_image_from_path(image_path)
        source = image_path
    else:
        image = load_image_from_url(image_uri)
        source = image_uri

    features = [get_document_text_detection_feature()]
    request = build_annotate_request(image, features, language_hints=language_hints)
    response = client.annotate_image(request)

    result = {
        "source": source,
        "full_text": "",
        "pages": [],
    }

    if response.full_text_annotation:
        result["full_text"] = response.full_text_annotation.text

        for page in response.full_text_annotation.pages:
            page_info = {
                "width": page.width,
                "height": page.height,
                "blocks": [],
            }

            for block in page.blocks:
                block_text = "".join(
                    word.text for p in block.paragraphs for word in p.words
                )
                page_info["blocks"].append({
                    "text": block_text,
                    "confidence": block.confidence,
                    "block_type": block.block_type.name,
                })

            result["pages"].append(page_info)

    return result


if __name__ == "__main__":
    import sys
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        texts = detect_text(image_path=target)
        output = [
            {"text": t.text, "confidence": t.confidence, "language": t.language}
            for t in texts
        ]
        print(json.dumps(output, indent=2))
