from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
AZURE_FORM_RECOGNIZER_MODEL = os.getenv("AZURE_FORM_RECOGNIZER_MODEL", "prebuilt-invoice")


class DocumentClientConfigError(RuntimeError):
    pass


def get_document_analysis_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentAnalysisClient:
    resolved_endpoint = endpoint or AZURE_FORM_RECOGNIZER_ENDPOINT
    resolved_key = key or AZURE_FORM_RECOGNIZER_KEY
    if not resolved_endpoint or not resolved_key:
        raise DocumentClientConfigError(
            "Missing Azure Form Recognizer configuration: AZURE_FORM_RECOGNIZER_ENDPOINT and AZURE_FORM_RECOGNIZER_KEY are required."
        )
    return DocumentAnalysisClient(
        endpoint=resolved_endpoint,
        credential=AzureKeyCredential(resolved_key),
    )


def load_document_bytes(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def begin_analysis(model_id: str, document_bytes: bytes) -> Any:
    client = get_document_analysis_client()
    return client.begin_analyze_document(model_id=model_id, document=document_bytes)


def to_base64_document(document_bytes: bytes) -> str:
    return base64.b64encode(document_bytes).decode("ascii")


def get_field_value(fields: Dict[str, Any], name: str, default: Any = None) -> Any:
    field = fields.get(name)
    if not field:
        return default
    for attr in ("value", "content"):
        if hasattr(field, attr):
            value = getattr(field, attr)
            if value is not None:
                return value
    return default


def get_field_confidence(fields: Dict[str, Any], name: str) -> Optional[float]:
    field = fields.get(name)
    if not field:
        return None
    return getattr(field, "confidence", None)
