import os
from typing import List, Dict, Any
from document_client import DocumentClient
from document_models import KeyValuePair, TextractResponseParser


def extract_key_value_pairs(image_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Extract key-value pairs from a form-like document using Amazon Textract.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        List of key-value pairs
    """
    # Initialize Textract client
    client = DocumentClient()

    # Call Textract AnalyzeDocument API with FORMS feature
    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["FORMS"]
    )

    # Parse key-value pairs from response
    pairs = TextractResponseParser.parse_key_value_pairs(response)

    # Convert to dictionary format
    result = []
    for pair in pairs:
        if pair.key and pair.value:  # Only include complete pairs
            result.append(
                {
                    "key": pair.key,
                    "value": pair.value,
                    "key_confidence": pair.key_confidence,
                    "value_confidence": pair.value_confidence,
                    "overall_confidence": (pair.key_confidence + pair.value_confidence)
                    / 2,
                }
            )

    return result


def extract_form_fields(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract form fields with detailed geometry and relationships.

    Args:
        image_bytes: Bytes of the document image

    Returns:
        Structured form field extraction
    """
    client = DocumentClient()

    response = client.analyze_document(
        document_bytes=image_bytes, feature_types=["FORMS"]
    )

    blocks = response.get("Blocks", [])

    # Find key-value relationships
    kv_pairs = []
    key_blocks = [
        b
        for b in blocks
        if b.get("BlockType") == "KEY_VALUE_SET" and "KEY" in b.get("EntityTypes", [])
    ]

    for key_block in key_blocks:
        key_text = ""
        value_text = ""

        # Extract key text
        for rel in key_block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                word_ids = rel.get("Ids", [])
                words = [
                    b
                    for b in blocks
                    if b.get("Id") in word_ids and b.get("BlockType") == "WORD"
                ]
                key_text = " ".join([w.get("Text", "") for w in words])

        # Find associated value blocks
        for rel in key_block.get("Relationships", []):
            if rel.get("Type") == "VALUE":
                value_ids = rel.get("Ids", [])
                for value_id in value_ids:
                    value_block = next(
                        (b for b in blocks if b.get("Id") == value_id), None
                    )
                    if value_block and "VALUE" in value_block.get("EntityTypes", []):
                        for v_rel in value_block.get("Relationships", []):
                            if v_rel.get("Type") == "CHILD":
                                v_word_ids = v_rel.get("Ids", [])
                                v_words = [
                                    b
                                    for b in blocks
                                    if b.get("Id") in v_word_ids
                                    and b.get("BlockType") == "WORD"
                                ]
                                value_text = " ".join(
                                    [w.get("Text", "") for w in v_words]
                                )

        if key_text and value_text:
            kv_pairs.append(
                {
                    "field_name": key_text.strip(),
                    "field_value": value_text.strip(),
                    "key_confidence": key_block.get("Confidence", 0.0),
                    "value_confidence": next(
                        (
                            b.get("Confidence", 0.0)
                            for b in blocks
                            if b.get("Id") in value_ids
                        ),
                        0.0,
                    )
                    if value_ids
                    else 0.0,
                }
            )

    return {
        "form_fields": kv_pairs,
        "total_fields": len(kv_pairs),
        "provider": "Amazon Textract",
    }
