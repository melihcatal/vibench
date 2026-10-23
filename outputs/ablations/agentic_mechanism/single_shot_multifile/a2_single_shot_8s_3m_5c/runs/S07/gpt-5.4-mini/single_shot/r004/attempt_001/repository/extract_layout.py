from document_client import build_azure_document_intelligence_client, get_poller_result
from document_models import DocumentImageRequest, normalize_layout_response, extract_layout_elements

MODEL_ID = "prebuilt-layout"


def extract_layout(image_path: str, endpoint: str | None = None, api_key: str | None = None) -> dict:
    request = DocumentImageRequest.from_path(image_path)
    client = build_azure_document_intelligence_client(endpoint=endpoint, api_key=api_key)
    poller = client.begin_analyze_document(MODEL_ID, body=request.data)
    result = get_poller_result(poller)
    elements = extract_layout_elements(result)
    return normalize_layout_response(elements=elements, raw=result)
