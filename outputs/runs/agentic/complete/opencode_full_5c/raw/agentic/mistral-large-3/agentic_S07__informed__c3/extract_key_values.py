from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
import os
from typing import List, Dict
from document_models import KeyValuePair, KeyValueResponse


def extract_key_values(
    image_path: str, mime_type: str = "image/jpeg"
) -> KeyValueResponse:
    """
    Extracts key-value pairs from a form-like document using Azure Document Intelligence.

    Args:
        image_path: Path to the document image file or URL.
        mime_type: MIME type of the document (e.g., "image/jpeg", "image/png").

    Returns:
        KeyValueResponse: Normalized response containing extracted key-value pairs.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type,
        )

    result: AnalyzeResult = poller.result()

    key_value_pairs = []
    for kv_pair in result.key_value_pairs or []:
        key_value_pairs.append(
            KeyValuePair(
                key=kv_pair.key.content if kv_pair.key else "",
                value=kv_pair.value.content if kv_pair.value else "",
                confidence=kv_pair.confidence,
            )
        )

    return KeyValueResponse(
        key_value_pairs=key_value_pairs, pages=len(result.pages) if result.pages else 0
    )
