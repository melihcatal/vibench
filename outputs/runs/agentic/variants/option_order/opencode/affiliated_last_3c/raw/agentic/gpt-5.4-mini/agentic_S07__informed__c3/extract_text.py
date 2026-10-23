from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_config
from document_models import DocumentRequest, DocumentResponse, normalize_text


def extract_text(request: DocumentRequest) -> DocumentResponse:
    cfg = get_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(cfg["endpoint"], AzureKeyCredential(cfg["key"]))
    with_bytes = request.content
    poller = client.begin_analyze_document(
        "prebuilt-read",
        analyze_request=with_bytes,
        content_type=request.mime_type,
        language=request.language_hints[0] if request.language_hints else None,
    )
    result = poller.result()
    text = normalize_text(getattr(result, "content", ""))
    return DocumentResponse(text=text, raw=result)
