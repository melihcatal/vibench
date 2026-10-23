from __future__ import annotations

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_client import load_azure_document_intelligence_config
from document_models import LayoutBlock, LayoutResponse, OCRRequest


def extract_layout(request: OCRRequest) -> LayoutResponse:
    config = load_azure_document_intelligence_config()
    client = DocumentIntelligenceClient(endpoint=config.endpoint, credential=AzureKeyCredential(config.key or ""))
    with open(request.document_path, "rb") as handle:
        poller = client.begin_analyze_document("prebuilt-layout", body=handle, content_type="application/octet-stream")
    result = poller.result()
    blocks = []
    for paragraph in getattr(result, "paragraphs", []) or []:
        blocks.append(
            LayoutBlock(
                kind=getattr(paragraph, "role", "paragraph") or "paragraph",
                text=getattr(paragraph, "content", ""),
                bounding_regions=[{"page_number": getattr(region, "page_number", None)} for region in getattr(paragraph, "bounding_regions", []) or []],
            )
        )
    return LayoutResponse(blocks=blocks, raw=result)
