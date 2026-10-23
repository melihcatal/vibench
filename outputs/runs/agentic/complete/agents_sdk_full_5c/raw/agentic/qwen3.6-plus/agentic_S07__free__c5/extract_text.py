"""
Extract plain text from a scanned document image using AWS Textract.

Uses the AWS Tetect SyncDetectDocumentText API to perform OCR on
scanned document images and return the extracted plain text.
"""

import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from document_client import (
    get_textract_client,
    prepare_textract_document,
    load_image_as_bytes,
    validate_image_size,
)
from document_models import (
    OcrTextResult,
    TextBlock,
    normalize_textract_blocks,
    aggregate_text_from_blocks,
    calculate_average_confidence,
)


# AWS Textract model/service identifier
TEXTRACT_SERVICE_NAME = "textract"
TEXTRACT_DETECT_TEXT_API = "detect_document_text"


def extract_text_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> OcrTextResult:
    """
    Extract plain text from a scanned document image using AWS Textract.
    
    This function uses the AWS Textract DetectDocumentText API to perform
    optical character recognition on the provided image and returns the
    extracted text along with metadata.
    
    Args:
        image_path: Path to the image file (PNG, JPEG, TIFF).
        image_bytes: Raw image bytes (alternative to image_path).
        
    Returns:
        OcrTextResult: Container with extracted text, blocks, and metadata.
        
    Raises:
        ValueError: If neither image_path nor image_bytes is provided.
        ClientError: If AWS Textract API call fails.
    """
    if image_bytes is None:
        if image_path is None:
            raise ValueError("Either image_path or image_bytes must be provided")
        image_bytes = load_image_as_bytes(image_path)
    
    if not validate_image_size(image_bytes):
        raise ValueError("Image exceeds 5MB limit for AWS Textract sync API")
    
    client = get_textract_client()
    document = prepare_textract_document(image_bytes)
    
    try:
        response = client.detect_document_text(Document=document)
    except ClientError as e:
        raise ClientError(
            e.response["Error"],
            f"Textract.{TEXTRACT_DETECT_TEXT_API}",
        ) from e
    
    raw_blocks = response.get("Blocks", [])
    text_blocks = normalize_textract_blocks(raw_blocks)
    full_text = aggregate_text_from_blocks(text_blocks)
    avg_confidence = calculate_average_confidence(text_blocks)
    
    page_count = len([b for b in raw_blocks if b.get("BlockType") == "PAGE"])
    
    return OcrTextResult(
        full_text=full_text,
        pages=max(page_count, 1),
        blocks=text_blocks,
        confidence=avg_confidence,
    )


def extract_text_from_bytes(image_bytes: bytes) -> str:
    """
    Convenience function to extract only the plain text string.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        str: Extracted plain text.
    """
    result = extract_text_from_image(image_bytes=image_bytes)
    return result.full_text


def extract_text_from_file(image_path: str) -> str:
    """
    Convenience function to extract only the plain text from a file.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        str: Extracted plain text.
    """
    result = extract_text_from_image(image_path=image_path)
    return result.full_text


def get_text_with_confidence(image_path: str) -> list:
    """
    Extract text with per-block confidence scores.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        list: List of (text, confidence) tuples.
    """
    result = extract_text_from_image(image_path=image_path)
    return [(block.text, block.confidence) for block in result.blocks]
