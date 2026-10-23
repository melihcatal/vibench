import os
from typing import Any, Dict
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import load_document_bytes, normalize_language, require_env
from document_models import extract_invoice_result


def extract_invoice_fields(source: str, *, locale: str | None = None) -> Dict[str, Any]:
    endpoint = require_env('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = require_env('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    document = load_document_bytes(source)
    poller = client.begin_analyze_document('prebuilt-invoice', body=document, locale=normalize_language(locale), content_type='application/octet-stream')
    result = poller.result()
    return extract_invoice_result(result)
