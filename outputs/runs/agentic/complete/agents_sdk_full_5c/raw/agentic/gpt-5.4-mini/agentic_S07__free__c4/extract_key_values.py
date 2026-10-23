from typing import Dict, Optional

from document_client import AzureDocumentIntelligenceClient, get_default_client
from document_models import KeyValueRequest, KeyValueResponse, normalize_document_result

AZURE_DOC_INTELLIGENCE_MODEL_ID = "prebuilt-layout"


def _build_payload(request: KeyValueRequest) -> Dict[str, object]:
    if request.image_url:
        return {"urlSource": request.image_url}
    if request.image_bytes_b64:
        return {"base64Source": request.image_bytes_b64}
    return {}


def extract_key_values(request: KeyValueRequest, client: Optional[AzureDocumentIntelligenceClient] = None) -> KeyValueResponse:
    client = client or get_default_client()
    response = client.post_analyze(AZURE_DOC_INTELLIGENCE_MODEL_ID, _build_payload(request))
    response.raise_for_status()
    operation_url = response.headers.get("operation-location")
    result = client.get_operation(operation_url)
    result.raise_for_status()
    raw = result.json()
    normalized = normalize_document_result(raw)
    key_values: Dict[str, str] = {}
    for item in normalized["keyValuePairs"]:
        key = (item.get("key") or {}).get("content", "")
        value = (item.get("value") or {}).get("content", "")
        if key:
            key_values[key] = value
    return KeyValueResponse(key_values=key_values, raw=raw)
