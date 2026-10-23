"""
Extract layout elements (blocks, lines, tables, selection marks) from a document
using Azure AI Document Intelligence.

Uses the azure-ai-documentintelligence SDK with the prebuilt-layout model to
identify structural elements including paragraphs, tables, headers, footers,
and list items with bounding box coordinates.
"""

from typing import Optional

from document_client import create_document_intelligence_client, read_file_bytes
from document_models import OcrLayoutResponse, normalize_azure_di_layout_response


def extract_layout_from_document(
    file_path: str,
    *,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> OcrLayoutResponse:
    """
    Extract layout elements from a document using Azure Document Intelligence layout analysis.

    Args:
        file_path: Path to the local document file.
        endpoint: Azure DI endpoint URL. Falls back to AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT.
        key: Azure DI API key. Falls back to AZURE_DOCUMENT_INTELLIGENCE_KEY.

    Returns:
        OcrLayoutResponse containing typed layout blocks with positions.
    """
    client = create_document_intelligence_client(endpoint=endpoint, key=key)
    file_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
    )
    result = poller.result()
    result_dict = result.as_dict()

    return normalize_azure_di_layout_response(result_dict)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        resp = extract_layout_from_document(sys.argv[1])
        for block in resp.layout_blocks:
            print(f"[{block.kind}] (page {block.page}) {block.content}")
    else:
        print("Usage: python extract_layout.py <path-to-document>")
