from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_config
from document_models import (
    DocumentRequest,
    DocumentResponse,
    normalize_key_values,
    normalize_text,
)


def extract_key_values(request: DocumentRequest) -> DocumentResponse:
    cfg = get_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(cfg["endpoint"], AzureKeyCredential(cfg["key"]))
    poller = client.begin_analyze_document(
        "prebuilt-document",
        analyze_request=request.content,
        content_type=request.mime_type,
    )
    result = poller.result()
    items = []
    for pair in getattr(result, "key_value_pairs", []) or []:
        items.append(
            {
                "key": normalize_text(
                    getattr(getattr(pair, "key", None), "content", "")
                ),
                "value": normalize_text(
                    getattr(getattr(pair, "value", None), "content", "")
                ),
            }
        )
    return DocumentResponse(
        key_values=normalize_key_values(items),
        text=normalize_text(getattr(result, "content", "")),
        raw=result,
    )
