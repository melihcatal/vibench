"""
[SAME-SCENARIO] Extract plain text from a scanned document image.
Uses Google Cloud Vision API DOCUMENT_TEXT_DETECTION for dense text extraction
from scanned images, receipts, forms, and other document types.
"""

import os
from typing import Optional, List
from google.cloud import vision_v1

from document_client import GoogleVisionClient, get_vision_client
from document_models import (
    OcrResponse,
    TextBlock,
    BoundingBox,
    normalize_vision_vertices,
    build_vision_image_context,
)


GOOGLE_CLOUD_VISION_MODEL = "builtin/latest"


def extract_text_from_image(
    image_path: str,
    language_hints: Optional[List[str]] = None,
    client: Optional[GoogleVisionClient] = None,
) -> OcrResponse:
    """
    Extract plain text from a scanned document image using Google Cloud Vision API.

    Uses DOCUMENT_TEXT_DETECTION which is optimized for dense text in documents.
    This model identifier is "builtin/latest" for Google Vision's document text detection.

    Args:
        image_path: Path to the scanned document image file.
        language_hints: Optional list of BCP-47 language codes (e.g., ["en", "es"]).
        client: Optional pre-configured GoogleVisionClient.

    Returns:
        OcrResponse containing full text and individual text blocks.
    """
    if client is None:
        client = get_vision_client()

    image_content = client.encode_image_to_base64(image_path)

    image_context = None
    if language_hints:
        image_context = build_vision_image_context(language_hints=language_hints)

    features = [client.create_feature("DOCUMENT_TEXT_DETECTION")]

    response = client.annotate_image(
        image_content=image_content,
        features=features,
        image_context=image_context,
    )

    return parse_ocr_response(response)


def parse_ocr_response(response: vision_v1.AnnotateImageResponse) -> OcrResponse:
    """Parse Google Vision API response into normalized OcrResponse model."""
    full_text = ""
    blocks = []

    if response.full_text_annotation:
        full_text = response.full_text_annotation.text

        page = response.full_text_annotation.pages[0] if response.full_text_annotation.pages else None
        page_width = 1.0
        page_height = 1.0
        if page and hasattr(page, 'width') and page.width:
            page_width = float(page.width)
        if page and hasattr(page, 'height') and page.height:
            page_height = float(page.height)

        for block in response.full_text_annotation.blocks:
            block_text = _extract_block_text(block)
            confidence = getattr(block, 'confidence', 0.0) or 0.0
            bounding_box = normalize_vision_vertices(block.bounding_box, page_width, page_height)

            block_type = _classify_block_type(block)

            language = _extract_block_language(block)

            blocks.append(
                TextBlock(
                    text=block_text.strip(),
                    confidence=confidence,
                    bounding_box=bounding_box,
                    block_type=block_type,
                    language=language,
                )
            )

    return OcrResponse(
        full_text=full_text.strip(),
        blocks=blocks,
        language="en",
        page_count=1,
    )


def _extract_block_text(block) -> str:
    """Extract concatenated text from a Google Vision block."""
    text_parts = []
    for paragraph in block.paragraphs:
        for word in paragraph.words:
            word_text = "".join(symbol.text for symbol in word.symbols)
            text_parts.append(word_text)
        text_parts.append(" ")
    return "".join(text_parts)


def _classify_block_type(block):
    """Classify block type based on Google Vision block property."""
    from document_models import BlockType

    block_type_prop = getattr(block, 'block_type', None)
    if block_type_prop is not None:
        type_name = vision_v1.Feature.Type(block_type_prop).name if hasattr(vision_v1.Feature.Type, '__call__') else str(block_type_prop)
        if "TITLE" in str(block_type_prop).upper():
            return BlockType.TITLE
        elif "LIST" in str(block_type_prop).upper():
            return BlockType.LIST_ITEM
        elif "TABLE" in str(block_type_prop).upper():
            return BlockType.TABLE

    first_block = block.paragraphs[0] if block.paragraphs else None
    if first_block and hasattr(first_block, 'paragraph'):
        if first_block.paragraph.bounding_box:
            return BlockType.TEXT

    return BlockType.TEXT


def _extract_block_language(block) -> str:
    """Extract the dominant language code from a Google Vision block."""
    if hasattr(block, 'property') and block.property:
        detected_languages = getattr(block.property, 'detected_languages', None)
        if detected_languages:
            for lang in detected_languages:
                if hasattr(lang, 'language_code') and lang.language_code:
                    return lang.language_code
    return "en"


if __name__ == "__main__":
    image_path = os.environ.get("OCR_IMAGE_PATH", "sample_document.png")
    result = extract_text_from_image(image_path)
    print(result.full_text)
