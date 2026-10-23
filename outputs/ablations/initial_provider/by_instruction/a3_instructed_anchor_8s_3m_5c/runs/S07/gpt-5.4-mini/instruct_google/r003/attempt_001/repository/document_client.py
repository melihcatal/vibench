import base64
import os
from typing import Any, Dict, Optional

from google.cloud import documentai


def _bytes_from_content(content: str) -> bytes:
    if os.path.exists(content):
        with open(content, "rb") as f:
            return f.read()
    return base64.b64decode(content)


def get_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def get_processor_name(project_id: Optional[str] = None, location: Optional[str] = None, processor_id: Optional[str] = None) -> str:
    project_id = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = processor_id or os.environ["GOOGLE_DOCUMENT_AI_PROCESSOR_ID"]
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"


def build_raw_document(content: str, mime_type: str = "image/png", language_hints: Optional[list[str]] = None) -> documentai.RawDocument:
    return documentai.RawDocument(content=_bytes_from_content(content), mime_type=mime_type, display_name=None)


def process_document(content: str, mime_type: str = "image/png", processor_id: Optional[str] = None, project_id: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
    client = get_document_ai_client()
    name = get_processor_name(project_id=project_id, location=location, processor_id=processor_id)
    raw_document = documentai.RawDocument(content=_bytes_from_content(content), mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    return {"document": result.document, "raw": result}
