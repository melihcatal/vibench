import os
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import TextBlock, TextractResponseParser


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract plain text from a scanned document image using Amazon Textract.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        Extracted text as a single string
    """
    # Initialize Textract client
    client = DocumentClient()

    # Call Textract DetectDocumentText API
    response = client.detect_document_text(image_bytes)

    # Parse response
    text_blocks = TextractResponseParser.parse_text_blocks(response)

    # Combine all text blocks
    full_text = "\n".join([block.text for block in text_blocks])

    return full_text


def extract_text_with_confidence(image_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extract text with confidence scores using Amazon Textract.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        List of dictionaries with text and confidence
    """
    client = DocumentClient()
    response = client.detect_document_text(image_bytes)

    text_blocks = TextractResponseParser.parse_text_blocks(response)

    result = []
    for block in text_blocks:
        result.append(
            {
                "text": block.text,
                "confidence": block.confidence,
                "block_type": block.block_type,
            }
        )

    return result
