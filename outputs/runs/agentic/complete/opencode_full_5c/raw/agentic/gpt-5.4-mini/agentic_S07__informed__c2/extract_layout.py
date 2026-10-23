from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import (
    get_azure_document_intelligence_endpoint,
    get_azure_document_intelligence_key,
    open_document_bytes,
)
from document_models import DocumentInput, LayoutResponse, normalize_blocks


def extract_layout(document: DocumentInput) -> LayoutResponse:
    client = DocumentIntelligenceClient(
        endpoint=get_azure_document_intelligence_endpoint(),
        credential=AzureKeyCredential(get_azure_document_intelligence_key()),
    )
    poller = client.begin_analyze_document(
        "prebuilt-layout", open_document_bytes(document.source)
    )
    result = poller.result()
    blocks = normalize_blocks(getattr(result, "paragraphs", []))
    return LayoutResponse(blocks=blocks, raw={"model_id": "prebuilt-layout"})
