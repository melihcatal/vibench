import base64
from typing import Dict, Optional

from document_client import AzureDocumentIntelligenceClient, get_default_client
from document_models import OCRRequest, OCRResponse, normalize_document_result

AZURE_DOC_INTELLIGENCE_MODEL_ID = "prebuilt-read"


def _build_payload(request: OCRRequest) -> Dict[str, object]:
    payload: Dict[str, object] = {}
    if request.image_url:
        payload["urlSource"] = request.image_url
    elif request.image_bytes_b64:
        payload["base64Source"] = request.image_bytes_b64
    if request.locale:
        payload["locale"] = request.locale
    return payload


def extract_text(request: OCRRequest, client: Optional[AzureDocumentIntelligenceClient] = None) -> OCRResponse:
    client = client or get_default_client()
    payload = _build_payload(request)
    response = client.post_analyze(AZURE_DOC_INTELLIGENCE_MODEL_ID, payload)
    response.raise_for_status()
    operation_url = response.headers.get("operation-location")
    if not operation_url:
        return OCRResponse(text="", raw={"error": "missing operation-location"})
    result = client.get_operation(operation_url)
    result.raise_for_status()
    raw = result.json()
    normalized = normalize_document_result(raw)
    text = "\n".join(p.get("content", "") for p in normalized["paragraphs"] if p.get("content"))
    if not text and normalized["pages"]:
        text = "\n".join(line.get("content", "") for page in normalized["pages"] for line in page.get("lines", []) if line.get("content"))
    return OCRResponse(text=text.strip(), raw=raw)
