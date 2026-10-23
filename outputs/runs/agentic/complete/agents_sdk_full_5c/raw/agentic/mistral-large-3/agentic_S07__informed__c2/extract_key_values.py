from typing import List, Dict, Any
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_intelligence_client
from document_models import KeyValueExtractionResponse


def extract_key_values_from_image(image_path: str, mime_type: str = "image/jpeg") -> KeyValueExtractionResponse:
    """Extract key-value pairs from a form-like document using Azure Document Intelligence."""
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-document",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
            content_type=mime_type
        )
    
    result: AnalyzeResult = poller.result()
    
    key_values = []
    for kv_pair in result.key_value_pairs:
        key_values.append({
            "key": kv_pair.key.content if kv_pair.key else "",
            "value": kv_pair.value.content if kv_pair.value else "",
            "confidence": kv_pair.confidence
        })
    
    return KeyValueExtractionResponse(key_values=key_values)