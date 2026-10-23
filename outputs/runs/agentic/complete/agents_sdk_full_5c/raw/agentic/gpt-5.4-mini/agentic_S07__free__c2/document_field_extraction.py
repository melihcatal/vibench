from __future__ import annotations

import os
from typing import Dict

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_models import NormalizedDocument

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
AZURE_CUSTOM_EXTRACTION_MODEL_ID = os.getenv("AZURE_CUSTOM_EXTRACTION_MODEL_ID", "prebuilt-document")


def extract_fields_from_document(normalized: NormalizedDocument) -> Dict[str, str]:
    if not AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT or not AZURE_DOCUMENT_INTELLIGENCE_KEY:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required")
    client = DocumentAnalysisClient(AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY))
    poller = client.begin_analyze_document(AZURE_CUSTOM_EXTRACTION_MODEL_ID, document=normalized.text.encode("utf-8"))
    result = poller.result()
    fields: Dict[str, str] = {}
    for kv in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(kv, "key", None), "content", "").strip()
        value = getattr(getattr(kv, "value", None), "content", "").strip()
        if key:
            fields[key] = value
    return fields
