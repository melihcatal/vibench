import os
from typing import Any, Dict

import requests

from document_client import load_document_client
from document_models import DocumentRequest, KeyValueExtractionResult, normalize_key_value_response

AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")


def extract_key_values(image_bytes: bytes, content_type: str = "application/octet-stream", api_version: str = "2023-07-31") -> KeyValueExtractionResult:
    client = load_document_client()
    request = DocumentRequest(image_bytes=image_bytes, content_type=content_type)
    result = client.extract_key_values(request=request, api_version=api_version)
    return normalize_key_value_response(result)


def azure_extract_key_values(image_bytes: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
    if not AZURE_FORM_RECOGNIZER_ENDPOINT or not AZURE_FORM_RECOGNIZER_KEY:
        raise RuntimeError("Azure Form Recognizer credentials are required")
    url = f"{AZURE_FORM_RECOGNIZER_ENDPOINT.rstrip('/')}/formrecognizer/documentModels/prebuilt-document:analyze?api-version=2023-07-31"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_FORM_RECOGNIZER_KEY,
        "Content-Type": content_type,
    }
    response = requests.post(url, headers=headers, data=image_bytes, timeout=60)
    response.raise_for_status()
    return {"operation-location": response.headers.get("operation-location", ""), "status_code": response.status_code}
