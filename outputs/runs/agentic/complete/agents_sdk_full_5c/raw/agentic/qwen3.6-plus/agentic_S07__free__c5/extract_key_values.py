"""
Extract key-value pairs from a form-like document using AWS Textract.

Uses the FORMS feature of AWS Textract AnalyzeDocument API to identify
and extract key-value pairs from forms, invoices, receipts, and other
structured documents.
"""

import os
from typing import Optional, List, Dict

import boto3
from botocore.exceptions import ClientError

from document_client import (
    get_textract_client,
    prepare_textract_document,
    load_image_as_bytes,
    validate_image_size,
)
from document_models import (
    KeyValueResult,
    KeyValue,
    normalize_textract_key_values,
)


# AWS Textract service and feature identifiers
TEXTRACT_SERVICE_NAME = "textract"
TEXTRACT_ANALYZE_DOCUMENT_API = "analyze_document"
TEXTRACT_FORMS_FEATURE = "FORMS"


def extract_key_values_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> KeyValueResult:
    """
    Extract key-value pairs from a form-like document using AWS Textract.
    
    This function uses the AWS Textract AnalyzeDocument API with the
    FORMS feature type to identify key-value pairs in forms, invoices,
    receipts, and other structured documents.
    
    Args:
        image_path: Path to the image file (PNG, JPEG, TIFF).
        image_bytes: Raw image bytes (alternative to image_path).
        
    Returns:
        KeyValueResult: Container with extracted key-value pairs.
        
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
        response = client.analyze_document(
            Document=document,
            FeatureTypes=[TEXTRACT_FORMS_FEATURE],
        )
    except ClientError as e:
        raise ClientError(
            e.response["Error"],
            f"Textract.{TEXTRACT_ANALYZE_DOCUMENT_API}",
        ) from e
    
    raw_blocks = response.get("Blocks", [])
    kv_blocks = [
        b for b in raw_blocks
        if b.get("BlockType") == "KEY_VALUE_SET"
    ]
    
    pairs = normalize_textract_key_values(kv_blocks, raw_blocks)
    
    page_count = len([b for b in raw_blocks if b.get("BlockType") == "PAGE"])
    
    return KeyValueResult(
        pairs=pairs,
        pages=max(page_count, 1),
    )


def extract_key_values_from_bytes(image_bytes: bytes) -> List[KeyValue]:
    """
    Convenience function to extract key-value pairs from image bytes.
    
    Args:
        image_bytes: Raw image bytes.
        
    Returns:
        List[KeyValue]: Extracted key-value pairs.
    """
    result = extract_key_values_from_image(image_bytes=image_bytes)
    return result.pairs


def extract_key_values_from_file(image_path: str) -> List[KeyValue]:
    """
    Convenience function to extract key-value pairs from a file.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[KeyValue]: Extracted key-value pairs.
    """
    result = extract_key_values_from_image(image_path=image_path)
    return result.pairs


def get_key_values_as_dict(image_path: str) -> Dict[str, str]:
    """
    Extract key-value pairs and return as a simple dictionary.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        Dict[str, str]: Dictionary mapping keys to values.
    """
    result = extract_key_values_from_image(image_path=image_path)
    return {pair.key: pair.value for pair in result.pairs}


def get_value_by_key(image_path: str, key: str) -> Optional[str]:
    """
    Look up a specific key and return its value.
    
    Args:
        image_path: Path to the image file.
        key: The key to look up.
        
    Returns:
        Optional[str]: The value for the key, or None if not found.
    """
    result = extract_key_values_from_image(image_path=image_path)
    for pair in result.pairs:
        if pair.key.lower() == key.lower():
            return pair.value
    return None


def get_keys_only(image_path: str) -> List[str]:
    """
    Extract only the keys from the document.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        List[str]: List of extracted keys.
    """
    result = extract_key_values_from_image(image_path=image_path)
    return [pair.key for pair in result.pairs]


def get_confident_pairs(image_path: str, min_confidence: float = 0.8) -> List[KeyValue]:
    """
    Extract key-value pairs that meet a minimum confidence threshold.
    
    Args:
        image_path: Path to the image file.
        min_confidence: Minimum confidence threshold (0.0 to 1.0).
        
    Returns:
        List[KeyValue]: Key-value pairs above the confidence threshold.
    """
    result = extract_key_values_from_image(image_path=image_path)
    return [
        pair for pair in result.pairs
        if pair.key_confidence >= min_confidence and pair.value_confidence >= min_confidence
    ]
