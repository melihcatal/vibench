from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_document_intelligence_config
from document_models import OCRRequest, OCRTextResponse


def extract_text(request: OCRRequest) -> OCRTextResponse:
    config = load_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(
        endpoint=config.endpoint,
        credential=AzureKeyCredential(config.key or ""),
    )
    with open(request.document_path, "rb") as handle:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            body=handle,
            content_type="application/octet-stream",
            locale=request.locale,
        )
    result = poller.result()
    text = getattr(result, "content", "") or "\n".join(
        [getattr(line, "content", "") for page in getattr(result, "pages", []) for line in getattr(page, "lines", [])]
    )
    return OCRTextResponse(text=text, pages=[{"page_number": getattr(page, "page_number", None)} for page in getattr(result, "pages", [])], raw=result)
