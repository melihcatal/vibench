from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from document_client import build_client
from document_models import OCRRequest, normalize_payload, normalize_tables


def extract_tables(request: OCRRequest):
    client = build_client()
    payload = (
        AnalyzeDocumentRequest(url_source=request.image_url)
        if request.image_url
        else request.image_bytes
    )
    poller = client.begin_analyze_document("prebuilt-layout", payload)
    result = poller.result()
    data = normalize_payload(result)
    return {"tables": normalize_tables(data), "raw": data}
