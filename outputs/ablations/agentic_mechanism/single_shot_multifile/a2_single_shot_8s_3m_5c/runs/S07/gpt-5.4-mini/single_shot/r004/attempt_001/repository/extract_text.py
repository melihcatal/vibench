import os
from document_client import build_azure_document_intelligence_client, get_poller_result, first_result_from_analyze
from document_models import DocumentImageRequest, normalize_text_response

MODEL_ID = "prebuilt-read"


def extract_text(image_path: str, endpoint: str | None = None, api_key: str | None = None) -> dict:
    request = DocumentImageRequest.from_path(image_path)
    client = build_azure_document_intelligence_client(endpoint=endpoint, api_key=api_key)
    poller = client.begin_analyze_document(MODEL_ID, body=request.data)
    result = get_poller_result(poller)
    text = first_result_from_analyze(result)
    return normalize_text_response(text=text, raw=result)


def extract_text_from_bytes(content: bytes, endpoint: str | None = None, api_key: str | None = None) -> dict:
    client = build_azure_document_intelligence_client(endpoint=endpoint, api_key=api_key)
    poller = client.begin_analyze_document(MODEL_ID, body=content)
    result = get_poller_result(poller)
    text = first_result_from_analyze(result)
    return normalize_text_response(text=text, raw=result)
