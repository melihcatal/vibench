from __future__ import annotations

import os
from typing import Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


DEFAULT_API_VERSION = "2024-11-30"


def get_document_intelligence_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> DocumentIntelligenceClient:
    service_endpoint = endpoint or os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    service_key = key or os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=service_endpoint,
        credential=AzureKeyCredential(service_key),
        api_version=DEFAULT_API_VERSION,
    )


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as file_obj:
        return file_obj.read()


def guess_content_type(path: str) -> str:
    lowered = path.lower()
    if lowered.endswith(".pdf"):
        return "application/pdf"
    if lowered.endswith(".png"):
        return "image/png"
    if lowered.endswith(".jpg") or lowered.endswith(".jpeg"):
        return "image/jpeg"
    if lowered.endswith(".tif") or lowered.endswith(".tiff"):
        return "image/tiff"
    if lowered.endswith(".bmp"):
        return "image/bmp"
    return "application/octet-stream"
