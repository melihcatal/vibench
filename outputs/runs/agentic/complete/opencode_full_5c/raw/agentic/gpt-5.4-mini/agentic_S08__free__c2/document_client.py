import os
from typing import Any, Dict

from google.cloud import documentai

from document_models import DocumentField, DocumentRequest, DocumentResponse


def get_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    return documentai.DocumentProcessorServiceClient()


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "")


def build_processor_path(location: str, processor_id: str) -> str:
    client = get_document_ai_client()
    return client.processor_path(get_project_id(), location, processor_id)


def parse_document_ai_response(document: Any, document_type: str) -> DocumentResponse:
    fields = []
    for name, field in getattr(document, "entities", []) or []:
        fields.append(
            DocumentField(
                name=name,
                value=getattr(field, "mention_text", None),
                confidence=getattr(field, "confidence", None),
            )
        )
    raw: Dict[str, Any] = document.__dict__ if hasattr(document, "__dict__") else {}
    return DocumentResponse(document_type=document_type, fields=fields, raw=raw)


def prepare_request(
    source_uri: str, document_type: str, schema_name: str
) -> DocumentRequest:
    return DocumentRequest(
        source_uri=source_uri, document_type=document_type, schema_name=schema_name
    )
