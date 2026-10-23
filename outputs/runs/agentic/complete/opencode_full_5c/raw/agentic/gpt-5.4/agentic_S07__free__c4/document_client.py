from __future__ import annotations

import base64
import os
from typing import Any

from google.cloud import documentai_v1 as documentai

from document_models import DocumentInput


DOCUMENT_AI_PROCESSOR_ENV = "GOOGLE_DOCUMENTAI_PROCESSOR"
DOCUMENT_AI_LOCATION_ENV = "GOOGLE_DOCUMENTAI_LOCATION"
DOCUMENT_AI_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def get_processor_name(
    processor_id: str | None = None,
    project_id: str | None = None,
    location: str | None = None,
) -> str:
    project = project_id or os.environ[DOCUMENT_AI_PROJECT_ENV]
    region = location or os.environ.get(DOCUMENT_AI_LOCATION_ENV, "us")
    processor = processor_id or os.environ[DOCUMENT_AI_PROCESSOR_ENV]
    return f"projects/{project}/locations/{region}/processors/{processor}"


def build_raw_document(document: DocumentInput) -> documentai.RawDocument:
    return documentai.RawDocument(
        content=document.content, mime_type=document.mime_type
    )


def build_process_request(
    document: DocumentInput, processor_name: str
) -> documentai.ProcessRequest:
    return documentai.ProcessRequest(
        name=processor_name, raw_document=build_raw_document(document)
    )


def read_document_bytes(path: str, mime_type: str | None = None) -> DocumentInput:
    with open(path, "rb") as handle:
        content = handle.read()
    resolved_mime = mime_type or _guess_mime_type(path)
    return DocumentInput(
        content=content, mime_type=resolved_mime, filename=os.path.basename(path)
    )


def to_base64_content(document: DocumentInput) -> str:
    return base64.b64encode(document.content).decode("utf-8")


def _guess_mime_type(path: str) -> str:
    lower = path.lower()
    if lower.endswith(".pdf"):
        return "application/pdf"
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".tif") or lower.endswith(".tiff"):
        return "image/tiff"
    return "application/octet-stream"


def document_to_dict(result: Any) -> dict[str, Any]:
    if hasattr(result, "_pb"):
        from google.protobuf.json_format import MessageToDict

        return MessageToDict(result._pb, preserving_proto_field_name=True)
    return {}
