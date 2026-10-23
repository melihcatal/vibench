from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import (
    get_azure_document_intelligence_endpoint,
    get_azure_document_intelligence_key,
    open_document_bytes,
)
from document_models import OCRResponse, DocumentInput, normalize_text


def extract_text(document: DocumentInput) -> OCRResponse:
    client = DocumentIntelligenceClient(
        endpoint=get_azure_document_intelligence_endpoint(),
        credential=AzureKeyCredential(get_azure_document_intelligence_key()),
    )
    poller = client.begin_analyze_document(
        "prebuilt-read", open_document_bytes(document.source)
    )
    result = poller.result()
    text = normalize_text(getattr(result, "content", ""))
    return OCRResponse(text=text, raw={"model_id": "prebuilt-read"})
