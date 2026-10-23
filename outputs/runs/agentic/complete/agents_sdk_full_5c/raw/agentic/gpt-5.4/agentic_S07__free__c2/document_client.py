from __future__ import annotations

import mimetypes
import os
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai


def get_google_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    api_endpoint = os.getenv("GOOGLE_CLOUD_LOCATION", "us").lower() + "-documentai.googleapis.com"
    return documentai.DocumentProcessorServiceClient(client_options=ClientOptions(api_endpoint=api_endpoint))


def get_processor_name(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> str:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = processor_id or os.environ["GOOGLE_DOCUMENTAI_PROCESSOR_ID"]
    client = get_google_document_ai_client()
    return client.processor_path(project_id, location, processor_id)


def read_document_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def guess_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "application/octet-stream"


def process_document(file_path: str, mime_type: Optional[str] = None):
    client = get_google_document_ai_client()
    raw_document = documentai.RawDocument(
        content=read_document_bytes(file_path),
        mime_type=mime_type or guess_mime_type(file_path),
    )
    request = documentai.ProcessRequest(
        name=get_processor_name(),
        raw_document=raw_document,
    )
    return client.process_document(request=request).document
