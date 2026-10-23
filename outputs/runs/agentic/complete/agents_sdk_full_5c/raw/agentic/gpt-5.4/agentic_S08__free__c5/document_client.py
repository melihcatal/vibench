from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


AZURE_FORM_RECOGNIZER_ENDPOINT_ENV = "AZURE_FORM_RECOGNIZER_ENDPOINT"
AZURE_FORM_RECOGNIZER_KEY_ENV = "AZURE_FORM_RECOGNIZER_KEY"
AZURE_FORM_RECOGNIZER_MODEL_ENV = "AZURE_FORM_RECOGNIZER_MODEL"
DEFAULT_AZURE_MODEL = "prebuilt-invoice"



def get_document_analysis_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DocumentAnalysisClient:
    resolved_endpoint = endpoint or os.environ[AZURE_FORM_RECOGNIZER_ENDPOINT_ENV]
    resolved_key = api_key or os.environ[AZURE_FORM_RECOGNIZER_KEY_ENV]
    credential = AzureKeyCredential(resolved_key)
    return DocumentAnalysisClient(endpoint=resolved_endpoint, credential=credential)



def get_model_id(default_model: str = DEFAULT_AZURE_MODEL) -> str:
    return os.getenv(AZURE_FORM_RECOGNIZER_MODEL_ENV, default_model)



def load_document_bytes(path: Optional[str] = None, content_base64: Optional[str] = None) -> bytes:
    if path:
        with open(path, "rb") as handle:
            return handle.read()
    if content_base64:
        return base64.b64decode(content_base64)
    raise ValueError("Either path or content_base64 must be provided")



def field_value(document: Any, name: str, attribute: str = "value") -> Dict[str, Any]:
    field = document.fields.get(name) if getattr(document, "fields", None) else None
    if not field:
        return {"value": None, "confidence": 0.0}
    value = getattr(field, attribute, None)
    if value is None:
        value = getattr(field, "content", None)
    return {"value": value, "confidence": float(getattr(field, "confidence", 0.0) or 0.0)}
