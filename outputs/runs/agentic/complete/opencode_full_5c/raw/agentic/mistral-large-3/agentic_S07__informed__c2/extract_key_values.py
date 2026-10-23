from typing import Dict, List, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeDocumentRequest,
    AnalyzeResult,
    DocumentKeyValuePair,
)
from azure.core.credentials import AzureKeyCredential


def extract_key_values(image_path: str) -> List[Dict]:
    """
    Extracts key-value pairs from a form-like document using Azure Document Intelligence.
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
        )

    result: AnalyzeResult = poller.result()

    key_value_pairs = []

    if result.key_value_pairs:
        for kv_pair in result.key_value_pairs:
            key = kv_pair.key.content if kv_pair.key else ""
            value = kv_pair.value.content if kv_pair.value else ""
            confidence = kv_pair.confidence if kv_pair.confidence else 0.0

            key_value_pairs.append(
                {"key": key, "value": value, "confidence": confidence}
            )

    return key_value_pairs
