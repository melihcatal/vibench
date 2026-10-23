"""
Extracts key-value pairs from a form-like document using AWS Textract.

Provider: AWS Textract (AnalyzeDocument API with FORMS feature)
Model/Feature: AWS Textract AnalyzeDocument with FORMS feature type
"""

import os
from typing import List

from document_client import (
    create_textract_client,
    load_image_bytes,
    build_textract_image_payload,
    normalize_textract_response,
)
from document_models import KeyValueResponse, KeyValueItem


# AWS Textract form extraction model identifier
TEXTRACT_FORMS_MODEL = "aws-textract-analyze-document-forms"

# Textract-specific block types for form processing
FORM_BLOCK_TYPES = ["KEY_VALUE_SET"]


def extract_key_values_from_image(image_path: str) -> KeyValueResponse:
    """
    Extract key-value pairs from a form document image using AWS Textract.

    Uses Textract's FORMS feature via AnalyzeDocument to detect form fields
    and associate keys with their corresponding values.

    Args:
        image_path: Path to the form document image file

    Returns:
        KeyValueResponse containing all detected key-value pairs
    """
    client = create_textract_client()
    image_bytes = load_image_bytes(image_path)
    payload = build_textract_image_payload(image_bytes)

    # AWS Textract AnalyzeDocument with FORMS feature
    response = client.analyze_document(
        Document=payload,
        FeatureTypes=["FORMS"]
    )

    normalized = normalize_textract_response(response)
    pairs = _parse_key_value_pairs(normalized["blocks"])

    page_blocks = [b for b in normalized["blocks"] if b.get("BlockType") == "PAGE"]
    page_count = max(len(page_blocks), 1)

    return KeyValueResponse(
        pairs=pairs,
        page_count=page_count,
        model_version=normalized.get("model_version", TEXTRACT_FORMS_MODEL),
        status_code=normalized.get("status_code", 0),
    )


def _parse_key_value_pairs(blocks: List[dict]) -> List[KeyValueItem]:
    """
    Parse Textract blocks into key-value pairs.

    Textract uses KEY_VALUE_SET blocks with EntityTypes to distinguish
    between KEY and VALUE blocks, with relationships linking them.

    Args:
        blocks: List of Textract Block dictionaries

    Returns:
        List of KeyValueItem objects
    """
    # Index blocks by ID for relationship traversal
    block_index = {b["Id"]: b for b in blocks if "Id" in b}

    # Separate key and value blocks
    key_blocks = []
    value_blocks = {}

    for block in blocks:
        if block.get("BlockType") != "KEY_VALUE_SET":
            continue

        entity_types = block.get("EntityTypes", [])

        if "KEY" in entity_types:
            key_blocks.append(block)
        elif "VALUE" in entity_types:
            # Use the block ID to track value blocks
            value_blocks[block["Id"]] = block

    pairs = []

    for key_block in key_blocks:
        key_text = _get_block_text(key_block, block_index)
        key_confidence = key_block.get("Confidence", 0.0)
        page = key_block.get("Page", 0)

        # Find associated value block via relationships
        value_text = ""
        value_confidence = 0.0

        relationships = key_block.get("Relationships", [])
        for rel in relationships:
            if rel.get("Type") == "VALUE":
                for value_id in rel.get("Ids", []):
                    value_block = value_blocks.get(value_id)
                    if value_block:
                        value_text = _get_block_text(value_block, block_index)
                        value_confidence = value_block.get("Confidence", 0.0)
                        break

        if key_text or value_text:
            pair = KeyValueItem(
                key=key_text,
                value=value_text,
                key_confidence=key_confidence,
                value_confidence=value_confidence,
                page=page,
            )
            pairs.append(pair)

    return pairs


def _get_block_text(block: dict, block_index: dict) -> str:
    """
    Extract text from a Textract KEY or VALUE block via its child relationships.

    Args:
        block: Textract KEY_VALUE_SET block
        block_index: Dictionary mapping block IDs to blocks

    Returns:
        Extracted text string
    """
    texts = []
    relationships = block.get("Relationships", [])

    for rel in relationships:
        if rel.get("Type") == "CHILD":
            for child_id in rel.get("Ids", []):
                child = block_index.get(child_id, {})
                child_text = child.get("Text", "")
                if child_text:
                    texts.append(child_text)

    return " ".join(texts).strip()


def find_value_by_key(pairs: List[KeyValueItem], key: str, case_sensitive: bool = False) -> str:
    """
    Find the value for a given key in extracted key-value pairs.

    Args:
        pairs: List of KeyValueItem objects
        key: Key string to search for
        case_sensitive: Whether to match case

    Returns:
        Value string if found, empty string otherwise
    """
    for pair in pairs:
        search_key = pair.key if case_sensitive else pair.key.lower()
        search_term = key if case_sensitive else key.lower()
        if search_key == search_term or search_term in search_key:
            return pair.value
    return ""


def pairs_to_dict(pairs: List[KeyValueItem], case_sensitive: bool = False) -> dict:
    """
    Convert list of KeyValueItem objects to a dictionary.

    Args:
        pairs: List of KeyValueItem objects
        case_sensitive: Whether to preserve key casing

    Returns:
        Dictionary mapping keys to values
    """
    result = {}
    for pair in pairs:
        key = pair.key if case_sensitive else pair.key.strip().lower()
        result[key] = {
            "value": pair.value,
            "key_confidence": pair.key_confidence,
            "value_confidence": pair.value_confidence,
        }
    return result


def filter_pairs_by_confidence(
    pairs: List[KeyValueItem],
    min_key_confidence: float = 0.0,
    min_value_confidence: float = 0.0,
) -> List[KeyValueItem]:
    """
    Filter key-value pairs by minimum confidence thresholds.

    Args:
        pairs: List of KeyValueItem objects
        min_key_confidence: Minimum confidence for key detection
        min_value_confidence: Minimum confidence for value detection

    Returns:
        Filtered list meeting both confidence thresholds
    """
    return [
        pair
        for pair in pairs
        if pair.key_confidence >= min_key_confidence
        and pair.value_confidence >= min_value_confidence
    ]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_key_values.py <image_path>")
        sys.exit(1)

    img_path = sys.argv[1]
    result = extract_key_values_from_image(img_path)

    print(f"Extracted {len(result.pairs)} key-value pair(s) from {result.page_count} page(s)")
    for i, pair in enumerate(result.pairs):
        print(f"  {i + 1}. {pair.key} = {pair.value} (key_conf: {pair.key_confidence:.1f}%, val_conf: {pair.value_confidence:.1f}%)")
