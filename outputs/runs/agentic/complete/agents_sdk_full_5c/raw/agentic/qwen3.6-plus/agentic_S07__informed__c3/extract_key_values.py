"""
Extract key-value pairs from a form-like document using Azure AI Document Intelligence.

Uses the azure-ai-documentintelligence SDK with the prebuilt-document model to
identify form fields and their associated values from structured documents such
as invoices, receipts, and forms.
"""

from typing import Optional

from document_client import create_document_intelligence_client, read_file_bytes
from document_models import OcrKeyValueResponse, normalize_azure_di_keyvalue_response


def extract_key_values_from_document(
    file_path: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> OcrKeyValueResponse:
    """
    Extract key-value pairs from a form document using Azure Document Intelligence.

    Args:
        file_path: Path to the local form document file.
        endpoint: Azure DI endpoint URL. Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.
        key: Azure DI API key. Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY.

    Returns:
        OcrKeyValueResponse containing detected key-value field pairs.
    """
    client = create_document_intelligence_client(endpoint=endpoint, key=key)
    file_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body=file_bytes,
    )
    result = poller.result()
    result_dict = result.as_dict()

    return normalize_azure_di_keyvalue_response(result_dict)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resp = extract_key_values_from_document(sys.argv[1])
        for kv in resp.key_value_pairs:
            print(f"{kv.key}: {kv.value} (conf={kv.confidence})")
    else:
        print("Usage: python extract_key_values.py <path-to-form-document>")
