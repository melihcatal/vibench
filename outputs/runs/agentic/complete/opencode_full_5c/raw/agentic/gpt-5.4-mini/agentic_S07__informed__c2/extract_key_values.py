from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import (
    get_azure_document_intelligence_endpoint,
    get_azure_document_intelligence_key,
    open_document_bytes,
)
from document_models import DocumentInput, KeyValueResponse


def extract_key_values(document: DocumentInput) -> KeyValueResponse:
    client = DocumentIntelligenceClient(
        endpoint=get_azure_document_intelligence_endpoint(),
        credential=AzureKeyCredential(get_azure_document_intelligence_key()),
    )
    poller = client.begin_analyze_document(
        "prebuilt-document", open_document_bytes(document.source)
    )
    result = poller.result()
    pairs = {}
    for item in getattr(result, "key_value_pairs", []) or []:
        key = getattr(getattr(item, "key", None), "content", "")
        value = getattr(getattr(item, "value", None), "content", "")
        if key:
            pairs[key] = value
    return KeyValueResponse(pairs=pairs, raw={"model_id": "prebuilt-document"})
