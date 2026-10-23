from typing import Any, Dict
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import load_document_bytes, require_env
from document_models import validate_structured_fields


def validate_document_fields(source: str) -> Dict[str, Any]:
    endpoint = require_env('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = require_env('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    document = load_document_bytes(source)
    poller = client.begin_analyze_document('prebuilt-layout', body=document, content_type='application/octet-stream')
    result = poller.result()
    return validate_structured_fields(result)
