from typing import Dict, List, Optional

from document_client import AzureDocumentIntelligenceClient, get_default_client
from document_models import LayoutRequest, LayoutResponse, normalize_document_result

AZURE_DOC_INTELLIGENCE_MODEL_ID = "prebuilt-layout"


def _build_payload(request: LayoutRequest) -> Dict[str, object]:
    payload: Dict[str, object] = {}
    if request.image_url:
        payload["urlSource"] = request.image_url
    elif request.image_bytes_b64:
        payload["base64Source"] = request.image_bytes_b64
    if request.features:
        payload["features"] = request.features
    return payload


def extract_layout(request: LayoutRequest, client: Optional[AzureDocumentIntelligenceClient] = None) -> LayoutResponse:
    client = client or get_default_client()
    response = client.post_analyze(AZURE_DOC_INTELLIGENCE_MODEL_ID, _build_payload(request))
    response.raise_for_status()
    operation_url = response.headers.get("operation-location")
    result = client.get_operation(operation_url)
    result.raise_for_status()
    raw = result.json()
    normalized = normalize_document_result(raw)
    blocks: List[Dict[str, object]] = []
    for paragraph in normalized["paragraphs"]:
        blocks.append({"type": "paragraph", **paragraph})
    for page in normalized["pages"]:
        for line in page.get("lines", []):
            blocks.append({"type": "line", "page": page.get("pageNumber"), **line})
    return LayoutResponse(blocks=blocks, raw=raw)
