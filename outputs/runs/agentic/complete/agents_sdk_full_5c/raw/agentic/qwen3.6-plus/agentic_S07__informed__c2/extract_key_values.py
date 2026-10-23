"""
Extracts key-value pairs from a form-like document using Azure AI Document Intelligence.
Uses the 'prebuilt-document' model for form analysis and key-value pair extraction.
"""

import os
from typing import List

from document_client import (
    create_document_client,
    read_image_bytes,
    normalize_azure_poller_response,
)
from document_models import (
    DocumentKeyValueResult,
    KeyValueEntry,
    normalize_key_value_result,
)

# Azure Document Intelligence prebuilt-document model for form/key-value extraction
AZURE_FORM_MODEL_ID = "prebuilt-document"


def extract_key_values_from_image(
    file_path: str,
    model_id: str = AZURE_FORM_MODEL_ID,
) -> DocumentKeyValueResult:
    """
    Extract key-value pairs from a form-like document using Azure AI Document Intelligence.

    Args:
        file_path: Path to the document image or PDF file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-document'.

    Returns:
        DocumentKeyValueResult: Normalized result containing extracted key-value pairs.

    Raises:
        ValueError: If required Azure environment variables are not set.
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    file_bytes = read_image_bytes(file_path)
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_key_value_result(result)
    return normalized


def extract_key_values_from_bytes(
    file_bytes: bytes,
    model_id: str = AZURE_FORM_MODEL_ID,
) -> DocumentKeyValueResult:
    """
    Extract key-value pairs from document bytes using Azure AI Document Intelligence.

    Args:
        file_bytes: Raw bytes of the document file.
        model_id: Azure Document Intelligence model ID. Defaults to 'prebuilt-document'.

    Returns:
        DocumentKeyValueResult: Normalized result containing extracted key-value pairs.
    """
    client = create_document_client()

    poller = client.begin_analyze_document(
        model_id=model_id,
        body={"base64Source": file_bytes.hex()},
    )

    result = normalize_azure_poller_response(poller)
    normalized = normalize_key_value_result(result)
    return normalized


def find_value_by_key(
    kv_result: DocumentKeyValueResult,
    search_key: str,
    case_insensitive: bool = True,
) -> List[KeyValueEntry]:
    """
    Find key-value entries matching a given key string.

    Args:
        kv_result: The full key-value extraction result.
        search_key: The key string to search for.
        case_insensitive: Whether to perform case-insensitive matching.

    Returns:
        List[KeyValueEntry]: Matching key-value entries.
    """
    matches = []
    for entry in kv_result.pairs:
        key_match = entry.key
        if case_insensitive:
            key_match = key_match.lower()
            search_key = search_key.lower()
        if search_key in key_match or key_match in search_key:
            matches.append(entry)
    return matches


def kv_pairs_to_dict(
    kv_result: DocumentKeyValueResult,
) -> dict:
    """
    Convert extracted key-value pairs to a simple Python dictionary.

    Args:
        kv_result: The full key-value extraction result.

    Returns:
        dict: Dictionary mapping keys to values (last value wins for duplicate keys).
    """
    result_dict = {}
    for entry in kv_result.pairs:
        result_dict[entry.key] = entry.value
    return result_dict
