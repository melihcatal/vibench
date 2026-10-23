from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client
from document_models import OCRRequest, OCRResponse, normalize_payload


def extract_text(request: OCRRequest) -> OCRResponse:
    client = build_client()
    payload = (
        AnalyzeDocumentRequest(url_source=request.image_url)
        if request.image_url
        else request.image_bytes
    )
    poller = client.begin_analyze_document("prebuilt-read", payload)
    result = poller.result()
    data = normalize_payload(result)
    text = getattr(result, "content", None) or data.get("content", "")
    return OCRResponse(text=text, raw=data)
