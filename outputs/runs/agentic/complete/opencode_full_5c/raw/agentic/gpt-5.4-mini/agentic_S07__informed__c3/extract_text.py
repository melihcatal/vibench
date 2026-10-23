import os
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import build_document_intelligence_client, coerce_document_bytes, default_polling_timeout
from document_models import OCRResult, normalize_ocr_result


def extract_text(document: Any, *, endpoint: Optional[str] = None, key: Optional[str] = None) -> OCRResult:
    client = build_document_intelligence_client(endpoint=endpoint, key=key)
    data = coerce_document_bytes(document)
    poller = client.begin_analyze_document("prebuilt-read", data, content_type="application/octet-stream")
    result = poller.result(timeout=default_polling_timeout())
    return normalize_ocr_result(result)
