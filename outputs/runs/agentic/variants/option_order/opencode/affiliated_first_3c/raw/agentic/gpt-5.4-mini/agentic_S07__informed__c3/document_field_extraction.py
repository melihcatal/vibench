from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client
from document_models import OCRRequest, normalize_payload


def extract_structured_fields(request: OCRRequest) -> dict:
    client = build_client()
    payload = (
        AnalyzeDocumentRequest(url_source=request.image_url)
        if request.image_url
        else request.image_bytes
    )
    poller = client.begin_analyze_document("prebuilt-document", payload)
    result = poller.result()
    data = normalize_payload(result)
    return {"fields": data.get("documents", []), "raw": data}
