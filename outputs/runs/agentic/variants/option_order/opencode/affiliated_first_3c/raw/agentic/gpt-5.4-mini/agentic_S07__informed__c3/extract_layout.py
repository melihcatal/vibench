from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client
from document_models import LayoutResponse, OCRRequest, normalize_payload


def extract_layout(request: OCRRequest) -> LayoutResponse:
    client = build_client()
    payload = (
        AnalyzeDocumentRequest(url_source=request.image_url)
        if request.image_url
        else request.image_bytes
    )
    poller = client.begin_analyze_document("prebuilt-layout", payload)
    result = poller.result()
    data = normalize_payload(result)
    return LayoutResponse(
        blocks=data.get("paragraphs", []) or data.get("blocks", []),
        lines=[
            item.get("content", "") if isinstance(item, dict) else str(item)
            for item in data.get("lines", [])
        ],
        tables=data.get("tables", []) or [],
        raw=data,
    )
