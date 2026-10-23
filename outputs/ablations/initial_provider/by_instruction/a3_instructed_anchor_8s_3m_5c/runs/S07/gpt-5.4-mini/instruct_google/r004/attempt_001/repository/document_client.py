import os
from typing import Any, Dict, Optional

from google.cloud import documentai


def get_config() -> Dict[str, Optional[str]]:
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        "processor_id": os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"),
    }


def get_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def build_processor_name(project_id: str, location: str, processor_id: str) -> str:
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def process_document(image_bytes: bytes, mime_type: str, processor_type: str, language_hints=None) -> Any:
    cfg = get_config()
    client = get_document_ai_client()
    name = build_processor_name(cfg["project_id"], cfg["location"], cfg["processor_id"])
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    return client.process_document(request=request)
