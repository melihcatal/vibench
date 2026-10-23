from __future__ import annotations

from typing import Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import NormalizedDocument


def extract_structured_fields(document: NormalizedDocument) -> Dict[str, str]:
    import os

    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document(model_id="prebuilt-document", body=document.text.encode("utf-8"))
    result = poller.result()
    fields: Dict[str, str] = {}
    for kv in getattr(result, "key_value_pairs", []) or []:
        key_text = getattr(getattr(kv, "key", None), "content", "").strip()
        value_text = getattr(getattr(kv, "value", None), "content", "").strip()
        if key_text:
            fields[key_text] = value_text
    return fields
