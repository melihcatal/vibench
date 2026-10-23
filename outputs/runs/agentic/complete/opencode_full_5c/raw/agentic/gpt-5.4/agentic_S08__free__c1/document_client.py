from __future__ import annotations

import os
from typing import Any, Dict, Optional

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

from document_models import DocumentSource


DEFAULT_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DEFAULT_PROCESSOR_ID = os.getenv("GOOGLE_DOCUMENTAI_PROCESSOR_ID")
DEFAULT_PROCESSOR_VERSION = os.getenv("GOOGLE_DOCUMENTAI_PROCESSOR_VERSION")


def get_documentai_client(
    location: Optional[str] = None,
) -> documentai.DocumentProcessorServiceClient:
    resolved_location = location or DEFAULT_LOCATION
    endpoint = f"{resolved_location}-documentai.googleapis.com"
    options = ClientOptions(api_endpoint=endpoint)
    return documentai.DocumentProcessorServiceClient(client_options=options)


def build_processor_name(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
    processor_version: Optional[str] = None,
) -> str:
    resolved_project = project_id or DEFAULT_PROJECT_ID
    resolved_location = location or DEFAULT_LOCATION
    resolved_processor = processor_id or DEFAULT_PROCESSOR_ID
    if not resolved_project or not resolved_processor:
        raise ValueError(
            "Missing Google Cloud Document AI project or processor configuration"
        )
    if processor_version or DEFAULT_PROCESSOR_VERSION:
        version = processor_version or DEFAULT_PROCESSOR_VERSION
        return f"projects/{resolved_project}/locations/{resolved_location}/processors/{resolved_processor}/processorVersions/{version}"
    return f"projects/{resolved_project}/locations/{resolved_location}/processors/{resolved_processor}"


def process_document(
    source: DocumentSource,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
    processor_version: Optional[str] = None,
    field_mask: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_documentai_client(location=location)
    name = build_processor_name(
        project_id=project_id,
        location=location,
        processor_id=processor_id,
        processor_version=processor_version,
    )
    raw_document = documentai.RawDocument(
        content=source.content_base64.encode("utf-8")
        if source.content_base64 and not source.gcs_uri
        else None,
        mime_type=source.mime_type,
    )
    request: Dict[str, Any] = {"name": name}
    if source.gcs_uri:
        gcs_document = documentai.GcsDocument(
            gcs_uri=source.gcs_uri, mime_type=source.mime_type
        )
        request["gcs_document"] = gcs_document
    else:
        request["raw_document"] = raw_document
    if field_mask:
        request["field_mask"] = field_mask
    result = client.process_document(request=request)
    return documentai.Document.to_dict(result.document)
