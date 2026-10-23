from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from typing import Optional, Tuple

from google.api_core.client_options import ClientOptions
from google.cloud import documentai


def load_document_bytes(path: str) -> Tuple[bytes, str]:
    file_path = Path(path)
    content = file_path.read_bytes()
    mime_type, _ = mimetypes.guess_type(file_path.name)
    return content, mime_type or "application/octet-stream"


def load_document_input(source: str, mime_type: Optional[str] = None) -> Tuple[bytes, str]:
    if os.path.exists(source):
        content, guessed = load_document_bytes(source)
        return content, mime_type or guessed
    try:
        return base64.b64decode(source), mime_type or "image/png"
    except Exception as exc:
        raise ValueError("source must be a filesystem path or base64-encoded payload") from exc


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    api_endpoint = os.getenv("GOOGLE_CLOUD_DOCUMENTAI_ENDPOINT", "us-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=ClientOptions(api_endpoint=api_endpoint))


def get_processor_name(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> str:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or os.getenv("DOCUMENTAI_LOCATION", "us")
    processor_id = processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def process_document(source: str, mime_type: Optional[str] = None, processor_name: Optional[str] = None):
    content, resolved_mime = load_document_input(source, mime_type)
    client = get_documentai_client()
    name = processor_name or get_processor_name()
    raw_document = documentai.RawDocument(content=content, mime_type=resolved_mime)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    return client.process_document(request=request).document
