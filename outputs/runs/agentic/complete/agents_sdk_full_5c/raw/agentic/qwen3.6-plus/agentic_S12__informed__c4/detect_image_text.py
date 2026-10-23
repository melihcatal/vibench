"""
detect_image_text.py - Detects text appearing inside an image (OCR)
using Google Cloud Vision API (google-cloud-vision SDK).

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import sys
from typing import List, Optional

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums as vision_enums

from vision_client import (
    VisionClientManager,
    build_image_source,
    build_image_source_from_url,
    build_image_context,
    fetch_image_as_bytes,
)
from vision_models import (
    ImageAnalysisRequest,
    TextDetectionResponse,
    TextDetectionResult,
)


def detect_text_in_image(
    image_url: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    language_hints: Optional[List[str]] = None,
) -> TextDetectionResponse:
    """Detect and extract text from an image using Google Cloud Vision OCR.

    Args:
        image_url: Public URL of the image to analyze.
        image_bytes: Raw image bytes (used if image_url is not provided).
        language_hints: Optional list of BCP-47 language codes for OCR hints.

    Returns:
        TextDetectionResponse with detected text blocks and full extracted text.
    """
    if not image_url and not image_bytes:
        raise ValueError("Either image_url or image_bytes must be provided.")

    client_manager = VisionClientManager()
    vision_client = client_manager.get_client()

    if image_url:
        image = build_image_source_from_url(image_url)
    else:
        image = build_image_source(image_bytes)

    # Build features for both dense and sparse text detection
    features = [
        vision_v1.Feature(
            type_=vision_enums.Feature.Type.TEXT_DETECTION,
            max_results=50,
        ),
        vision_v1.Feature(
            type_=vision_enums.Feature.Type.DOCUMENT_TEXT_DETECTION,
            max_results=10,
        ),
    ]

    context = build_image_context(language_hints=language_hints or ["en"])

    request = vision_v1.AnnotateImageRequest()
    request.image = image
    request.features = features
    request.image_context = context

    response = vision_client.annotate_image(request=request)

    texts: List[TextDetectionResult] = []
    full_text = ""

    # Use DOCUMENT_TEXT_DETECTION for structured text blocks (preferred for documents)
    if response.full_text_annotation and response.full_text_annotation.text:
        full_text = response.full_text_annotation.text.strip()

        # Extract individual word-level results from pages/blocks
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_type_map = {
                    vision_enums.Block.BlockType.TEXT: "text",
                    vision_enums.Block.BlockType.TABLE: "table",
                    vision_enums.Block.BlockType.PICTURE: "picture",
                    vision_enums.Block.BlockType.RULING_LINE: "ruling_line",
                    vision_enums.Block.BlockType.BARCODE: "barcode",
                    vision_enums.Block.BlockType.UNKNOWN: "unknown",
                }
                block_type_str = block_type_map.get(block.block_type, "text")

                for paragraph in block.paragraphs:
                    for word_info in paragraph.words:
                        word_text = "".join(
                            sym.text for sym in word_info.symbols
                        )
                        word_conf = getattr(word_info, "confidence", 1.0) or 1.0

                        bbox = None
                        if word_info.bounding_box:
                            vertices = word_info.bounding_box.vertices
                            bbox = [
                                {"x": v.x, "y": v.y} for v in vertices
                            ]

                        texts.append(
                            TextDetectionResult(
                                text=word_text,
                                confidence=word_conf,
                                bounding_box=bbox,
                                block_type=block_type_str,
                            )
                        )

    # Fallback to basic TEXT_DETECTION if full_text_annotation is empty
    if not full_text and response.text_annotations:
        # First element contains full detected text
        full_text = response.text_annotations[0].description.strip()
        for annotation in response.text_annotations[1:]:
            texts.append(
                TextDetectionResult(
                    text=annotation.description,
                    confidence=annotation.score or 1.0,
                    block_type="word",
                )
            )

    return TextDetectionResponse(
        texts=texts,
        full_text=full_text,
        raw_response={"status": "ok", "provider": "google-cloud-vision"},
    )


def detect_text_from_file(
    filepath: str,
    language_hints: Optional[List[str]] = None,
) -> TextDetectionResponse:
    """Detect text from a local image file using Google Cloud Vision OCR."""
    with open(filepath, "rb") as fh:
        image_bytes = fh.read()
    return detect_text_in_image(
        image_bytes=image_bytes, language_hints=language_hints
    )


def format_text_report(response: TextDetectionResponse) -> str:
    """Format a human-readable text detection report."""
    lines = ["=== Image Text Detection Report (Google Cloud Vision) ===", ""]
    lines.append(f"Full extracted text:\n  {response.full_text or '(none)'}")
    lines.append("")
    lines.append(f"Total text blocks detected: {len(response.texts)}")
    if response.texts:
        lines.append("")
        lines.append("Individual detections:")
        for i, t in enumerate(response.texts[:20], 1):
            lines.append(
                f"  {i}. \"{t.text}\" (confidence: {t.confidence:.4f}, type: {t.block_type})"
            )
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_url_or_file> [lang_hint]")
        sys.exit(1)

    source = sys.argv[1]
    hints = [sys.argv[2]] if len(sys.argv) > 2 else None

    if source.startswith(("http://", "https://")):
        result = detect_text_in_image(image_url=source, language_hints=hints)
    else:
        result = detect_text_from_file(source, language_hints=hints)

    print(format_text_report(result))
