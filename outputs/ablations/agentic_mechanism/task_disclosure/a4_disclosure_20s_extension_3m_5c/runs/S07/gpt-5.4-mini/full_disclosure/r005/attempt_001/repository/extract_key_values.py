import os
from typing import Any, Dict, List, Optional

from google.cloud import documentai_v1 as documentai


def _project_location_processor_path(project_id: str, location: str, processor_id: str) -> str:
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def _get_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def extract_key_values_from_bytes(
    content: bytes,
    mime_type: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]

    client = _get_client()
    name = _project_location_processor_path(project_id, location, processor_id)
    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    fields: List[Dict[str, Any]] = []
    document = result.document
    for entity in document.entities:
        key = entity.type_ or ""
        value = entity.mention_text or ""
        confidence = float(entity.confidence) if entity.confidence is not None else None
        fields.append({"key": key, "value": value, "confidence": confidence})
    return fields


def extract_key_values_from_uri(
    gcs_uri: str,
    mime_type: str,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    processor_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = processor_id or os.environ["DOCUMENTAI_PROCESSOR_ID"]

    client = _get_client()
    name = _project_location_processor_path(project_id, location, processor_id)
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    input_config = documentai.InputConfig(gcs_documents=documentai.GcsDocuments(documents=[gcs_document]))
    request = documentai.ProcessRequest(name=name, input_documents=input_config)
    result = client.process_document(request=request)

    fields: List[Dict[str, Any]] = []
    document = result.document
    for entity in document.entities:
        key = entity.type_ or ""
        value = entity.mention_text or ""
        confidence = float(entity.confidence) if entity.confidence is not None else None
        fields.append({"key": key, "value": value, "confidence": confidence})
    return fields
