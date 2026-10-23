"""
Extracts plain text from a scanned document image using AWS Textract.

Provider: AWS Textract (DetectDocumentText / AnalyzeDocument with TEXT feature)
Model/Feature: AWS Textract AnalyzeDocument API with TEXT detection
"""

import os
from typing import List

from document_client import (
    create_textract_client,
    load_image_bytes,
    build_textract_image_payload,
    normalize_textract_response,
)
from document_models import OCRRequest, OCRResponse, OCRTextBlock


# AWS Textract AnalyzeDocument model version identifier
TEXTRACT_DOCUMENT_MODEL = "aws-textract-analyze-document"

# Provider-specific feature types for Textract
TEXTRACT_FEATURE_TYPES = ["TABLES", "FORMS", "QUERIES"]


def extract_text_from_image(image_path: str) -> OCRResponse:
    """
    Extract plain text from a scanned document image using AWS Textract AnalyzeDocument.

    Uses the Textract AnalyzeDocument API with TEXT detection to extract
    all textual content from the provided document image.

    Args:
        image_path: Path to the scanned document image file

    Returns:
        OCRResponse containing extracted text blocks and concatenated text
    """
    client = create_textract_client()
    image_bytes = load_image_bytes(image_path)
    payload = build_textract_image_payload(image_bytes)

    # AWS Textract AnalyzeDocument API call
    response = client.analyze_document(
        Document=payload,
        FeatureTypes=["TABLES", "FORMS"]
    )

    normalized = normalize_textract_response(response)
    text_blocks = _parse_text_blocks(normalized["blocks"])

    full_text = " ".join(block.text for block in text_blocks if block.text.strip())

    # Determine page count from PAGE blocks
    page_blocks = [b for b in normalized["blocks"] if b.get("BlockType") == "PAGE"]
    page_count = max(len(page_blocks), 1)

    return OCRResponse(
        text_blocks=text_blocks,
        full_text=full_text.strip(),
        page_count=page_count,
        model_version=normalized.get("model_version", TEXTRACT_DOCUMENT_MODEL),
        status_code=normalized.get("status_code", 0),
    )


def _parse_text_blocks(blocks: List[dict]) -> List[OCRTextBlock]:
    """
    Parse Textract blocks into normalized OCR text blocks.

    Args:
        blocks: List of Textract Block dictionaries

    Returns:
        List of OCRTextBlock objects containing LINE and WORD level text
    """
    text_blocks = []

    for block in blocks:
        block_type = block.get("BlockType", "")

        if block_type in ("LINE", "WORD"):
            geometry = block.get("Geometry", {})
            ocr_block = OCRTextBlock(
                text=block.get("Text", ""),
                confidence=block.get("Confidence", 0.0),
                block_type=block_type,
                page=block.get("Page", 0),
                geometry=geometry.get("BoundingBox", None),
            )
            text_blocks.append(ocr_block)

    return text_blocks


def extract_text_to_file(image_path: str, output_path: str) -> str:
    """
    Extract text from image and write to output text file.

    Args:
        image_path: Path to scanned document image
        output_path: Path for output text file

    Returns:
        Path to the written text file
    """
    response = extract_text_from_image(image_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.full_text)
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <image_path> [output_path]")
        sys.exit(1)

    img_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "extracted_text.txt"

    result = extract_text_from_image(img_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result.full_text)
    print(f"Extracted {len(result.text_blocks)} text blocks to {out_path}")
