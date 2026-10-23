from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_config
from document_models import DocumentRequest, DocumentResponse, normalize_text


def extract_layout(request: DocumentRequest) -> DocumentResponse:
    cfg = get_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(cfg["endpoint"], AzureKeyCredential(cfg["key"]))
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request=request.content,
        content_type=request.mime_type,
    )
    result = poller.result()
    blocks = []
    for paragraph in getattr(result, "paragraphs", []) or []:
        blocks.append(
            {
                "role": getattr(paragraph, "role", None),
                "content": normalize_text(getattr(paragraph, "content", "")),
            }
        )
    lines = [
        normalize_text(line.content) for line in getattr(result, "lines", []) or []
    ]
    return DocumentResponse(
        text=normalize_text(getattr(result, "content", "")),
        blocks=blocks,
        lines=lines,
        raw=result,
    )
