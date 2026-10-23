from __future__ import annotations

import os
from typing import Optional

from google.cloud import documentai


def get_documentai_client(
    api_endpoint: Optional[str] = None,
) -> documentai.DocumentProcessorServiceClient:
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    endpoint = api_endpoint or os.getenv(
        "DOCUMENTAI_API_ENDPOINT",
        f"{location}-documentai.googleapis.com",
    )
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": endpoint}
    )


def get_processor_resource_name(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> str:
    resolved_project = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    resolved_location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    resolved_processor = processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]
    return f"projects/{resolved_project}/locations/{resolved_location}/processors/{resolved_processor}"


def build_raw_document(file_bytes: bytes, mime_type: str) -> documentai.RawDocument:
    return documentai.RawDocument(content=file_bytes, mime_type=mime_type)


def process_document_bytes(
    file_bytes: bytes,
    mime_type: str,
    processor_id: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
):
    client = get_documentai_client()
    name = get_processor_resource_name(project_id, location, processor_id)
    request = documentai.ProcessRequest(
        name=name,
        raw_document=build_raw_document(file_bytes, mime_type),
    )
    return client.process_document(request=request)
